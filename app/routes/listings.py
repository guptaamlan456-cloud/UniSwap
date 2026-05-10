from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.constants.options import AREA_OPTIONS, UNIVERSITY_OPTIONS
from app.forms.listing_forms import ListingForm
from app.models.listing import Listing

listings_bp = Blueprint("listings", __name__, url_prefix="/listings")


def _split_select_value(value, choices):
    if value in choices:
        return value, ""
    return "Other", value or ""


def _pick_value(select_value, other_value):
    if select_value == "Other":
        return (other_value or "").strip()
    return select_value


@listings_bp.route("/")
def browse():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("q", "")
    sort = request.args.get("sort", "default")
    area = request.args.get("area", "all")
    query = Listing.query.filter_by(is_active=True)
    if current_user.is_authenticated:
        query = query.filter(Listing.seller_id != current_user.id)
    if area != "all" and area in AREA_OPTIONS:
        query = query.filter(Listing.location == area)
    if search:
        query = query.filter(Listing.title.ilike(f"%{search}%"))
    if sort == "price_low":
        query = query.order_by(Listing.price.asc())
    elif sort == "price_high":
        query = query.order_by(Listing.price.desc())
    elif sort == "free_first":
        query = query.filter(Listing.free.is_(True)).order_by(Listing.departure_date.asc())
    else:
        query = query.order_by(Listing.departure_date.asc())
    listings = query.paginate(page=page, per_page=9)
    return render_template(
        "listings/listings.html",
        listings=listings,
        search=search,
        sort=sort,
        area=area,
        area_options=AREA_OPTIONS,
    )


@listings_bp.route("/<int:listing_id>")
def view(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template("listings/view.html", listing=listing)


@listings_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_listing():
    form = ListingForm()
    if request.method == "GET" and current_user.is_authenticated:
        form.location.data, form.location_other.data = _split_select_value(
            current_user.location, AREA_OPTIONS
        )
        form.university.data, form.university_other.data = _split_select_value(
            current_user.university, UNIVERSITY_OPTIONS
        )
        form.urgency_level.data = "medium"
    if form.validate_on_submit():
        location_value = _pick_value(form.location.data, form.location_other.data)
        university_value = _pick_value(form.university.data, form.university_other.data)
        listing = Listing(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            condition=form.condition.data,
            location=location_value,
            university=university_value,
            urgency_level=form.urgency_level.data,
            departure_date=form.departure_date.data,
            free=form.free.data,
            seller_id=current_user.id,
        )
        try:
            uploaded_urls = form.upload_images()
            listing.set_image_urls(uploaded_urls)
        except Exception:
            flash("Image upload failed. Listing saved without new images.", "warning")

        db.session.add(listing)
        db.session.commit()
        flash("Listing created successfully.", "success")
        return redirect(url_for("listings.my_listings"))

    return render_template("listings/create.html", form=form)


@listings_bp.route("/mine")
@login_required
def my_listings():
    listings = current_user.listings.order_by(Listing.created_at.desc()).all()
    return render_template("listings/my_listings.html", listings=listings)


@listings_bp.route("/<int:listing_id>/edit", methods=["GET", "POST"])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.seller_id != current_user.id:
        flash("You can only edit your own listings.", "danger")
        return redirect(url_for("listings.view", listing_id=listing.id))

    form = ListingForm(obj=listing)
    if request.method == "GET":
        form.location.data, form.location_other.data = _split_select_value(
            listing.location, AREA_OPTIONS
        )
        form.university.data, form.university_other.data = _split_select_value(
            listing.university, UNIVERSITY_OPTIONS
        )
    if form.validate_on_submit():
        location_value = _pick_value(form.location.data, form.location_other.data)
        university_value = _pick_value(form.university.data, form.university_other.data)
        listing.title = form.title.data
        listing.description = form.description.data
        listing.price = form.price.data
        listing.category = form.category.data
        listing.condition = form.condition.data
        listing.location = location_value
        listing.university = university_value
        listing.urgency_level = form.urgency_level.data
        listing.departure_date = form.departure_date.data
        listing.free = form.free.data

        current_urls = [] if form.clear_images.data else listing.get_image_urls()
        try:
            uploaded_urls = form.upload_images()
            listing.set_image_urls(current_urls + uploaded_urls)
        except Exception:
            flash("Some images failed to upload. Other changes were saved.", "warning")

        db.session.commit()
        flash("Listing updated successfully.", "success")
        return redirect(url_for("listings.view", listing_id=listing.id))

    return render_template("listings/edit.html", form=form, listing=listing)


@listings_bp.route("/<int:listing_id>/delete", methods=["POST"])
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.seller_id != current_user.id:
        flash("You can only delete your own listings.", "danger")
        return redirect(url_for("listings.view", listing_id=listing.id))
    db.session.delete(listing)
    db.session.commit()
    flash("Listing deleted successfully.", "success")
    return redirect(url_for("listings.my_listings"))
