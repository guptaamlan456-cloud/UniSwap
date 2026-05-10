from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db
from app.forms.chat_forms import ChatMessageForm, OfferActionForm
from app.models.chat_thread import ChatThread
from app.models.listing import Listing
from app.models.message import Message

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


def _is_thread_member(thread):
    return current_user.id in (thread.seller_id, thread.buyer_id)


@chat_bp.route("/")
@login_required
def inbox():
    threads = (
        ChatThread.query.filter(
            or_(ChatThread.seller_id == current_user.id, ChatThread.buyer_id == current_user.id)
        )
        .order_by(ChatThread.updated_at.desc())
        .all()
    )
    return render_template("chat/inbox.html", threads=threads)


@chat_bp.route("/listing/<int:listing_id>/start", methods=["POST"])
@login_required
def start_chat(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.seller_id == current_user.id:
        flash("You cannot message yourself on your own listing.", "warning")
        return redirect(url_for("listings.view", listing_id=listing.id))
    if not listing.is_active:
        flash("This listing is no longer active.", "warning")
        return redirect(url_for("listings.view", listing_id=listing.id))

    thread = ChatThread.query.filter_by(
        listing_id=listing.id, seller_id=listing.seller_id, buyer_id=current_user.id
    ).first()
    if not thread:
        thread = ChatThread(
            listing_id=listing.id,
            seller_id=listing.seller_id,
            buyer_id=current_user.id,
            status="open",
        )
        db.session.add(thread)
        db.session.commit()
    return redirect(url_for("chat.thread_view", thread_id=thread.id))


@chat_bp.route("/thread/<int:thread_id>", methods=["GET", "POST"])
@login_required
def thread_view(thread_id):
    thread = ChatThread.query.get_or_404(thread_id)
    if not _is_thread_member(thread):
        flash("You do not have access to this chat.", "danger")
        return redirect(url_for("chat.inbox"))

    message_form = ChatMessageForm()
    action_form = OfferActionForm()

    if message_form.validate_on_submit():
        if thread.status != "open":
            flash("This offer is already closed.", "warning")
            return redirect(url_for("chat.thread_view", thread_id=thread.id))
        message = Message(
            body=message_form.message.data,
            sender_id=current_user.id,
            listing_id=thread.listing_id,
            thread_id=thread.id,
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("chat.thread_view", thread_id=thread.id))

    messages = thread.messages.order_by(Message.created_at.asc()).all()
    return render_template(
        "chat/thread.html",
        thread=thread,
        messages=messages,
        message_form=message_form,
        action_form=action_form,
    )


@chat_bp.route("/thread/<int:thread_id>/offer/<string:action>", methods=["POST"])
@login_required
def offer_action(thread_id, action):
    thread = ChatThread.query.get_or_404(thread_id)
    form = OfferActionForm()
    if not form.validate_on_submit():
        return redirect(url_for("chat.thread_view", thread_id=thread.id))

    if current_user.id != thread.seller_id:
        flash("Only the seller can accept or decline offers.", "danger")
        return redirect(url_for("chat.thread_view", thread_id=thread.id))

    if thread.status != "open":
        flash("This offer is already closed.", "warning")
        return redirect(url_for("chat.thread_view", thread_id=thread.id))

    if action == "accept":
        thread.status = "accepted"
        thread.listing.is_active = False
        # Any other open offers on the same listing are auto-declined.
        (
            ChatThread.query.filter(
                ChatThread.listing_id == thread.listing_id,
                ChatThread.id != thread.id,
                ChatThread.status == "open",
            ).update({"status": "declined"}, synchronize_session=False)
        )
        flash("Offer accepted. Listing is now unlisted.", "success")
    elif action == "decline":
        thread.status = "declined"
        flash("Offer declined.", "info")
    else:
        flash("Unknown action.", "danger")

    db.session.commit()
    return redirect(url_for("chat.thread_view", thread_id=thread.id))
