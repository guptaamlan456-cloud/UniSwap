from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.constants.options import AREA_OPTIONS, UNIVERSITY_OPTIONS
from app.forms.auth_forms import EditProfileForm
from app.models.listing import Listing

main_bp = Blueprint("main", __name__)


def _split_select_value(value, choices):
    if value in choices:
        return value, ""
    return "Other", value or ""


def _pick_value(select_value, other_value):
    if select_value == "Other":
        return (other_value or "").strip()
    return select_value


@main_bp.route("/")
def index():
    featured_listings = (
        Listing.query.filter_by(is_active=True)
        .order_by(Listing.created_at.desc())
        .limit(8)
        .all()
    )
    my_listings = []
    if current_user.is_authenticated:
        my_listings = current_user.listings.order_by(Listing.created_at.desc()).all()
    return render_template(
        "main/index.html",
        featured_listings=featured_listings,
        my_listings=my_listings,
    )


@main_bp.route("/profile")
@login_required
def profile():
    my_listings_count = current_user.listings.count()
    return render_template("main/profile.html", my_listings_count=my_listings_count)


@main_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if request.method == "GET":
        form.location.data, form.location_other.data = _split_select_value(
            current_user.location, AREA_OPTIONS
        )
        form.university.data, form.university_other.data = _split_select_value(
            current_user.university, UNIVERSITY_OPTIONS
        )
    if form.validate_on_submit():
        location_value = _pick_value(form.location.data, form.location_other.data)
        university_value = _pick_value(form.university.data, form.university_other.data)
        current_user.name = form.name.data
        current_user.location = location_value
        current_user.university = university_value
        for listing in current_user.listings.all():
            listing.location = current_user.location
            listing.university = current_user.university
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("main.profile"))
    return render_template("main/edit_profile.html", form=form)


@main_bp.route("/nancy/search")
def nancy_search():
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"found": False, "message": "Please enter a product name."})

    found = (
        Listing.query.filter(Listing.is_active.is_(True))
        .filter(Listing.title.ilike(f"%{query}%"))
        .first()
        is not None
    )
    return jsonify(
        {
            "found": found,
            "url": url_for("listings.browse", q=query, sort="price_low"),
            "message": (
                f"I found listings for '{query}'. Taking you there now."
                if found
                else "Sorry, the product you are looking for is not listed at the moment."
            ),
        }
    )
