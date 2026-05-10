from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from app.forms.auth_forms import LoginForm, RegisterForm
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _pick_value(select_value, other_value):
    if select_value == "Other":
        return (other_value or "").strip()
    return select_value


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main.index"))
        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        location_value = _pick_value(form.location.data, form.location_other.data)
        university_value = _pick_value(form.university.data, form.university_other.data)
        user = User(
            name=form.name.data,
            email=form.email.data.lower(),
            location=location_value,
            university=university_value,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
