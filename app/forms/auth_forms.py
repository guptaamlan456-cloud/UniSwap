from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import ValidationError

from app.constants.options import AREA_OPTIONS, UNIVERSITY_OPTIONS, with_other


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    location = SelectField("Area", choices=with_other(AREA_OPTIONS), validators=[DataRequired()])
    location_other = StringField("Other Area", validators=[Length(max=120)])
    university = SelectField(
        "University", choices=with_other(UNIVERSITY_OPTIONS), validators=[DataRequired()]
    )
    university_other = StringField("Other University", validators=[Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Register")

    def validate_location_other(self, field):
        if self.location.data == "Other" and not (field.data or "").strip():
            raise ValidationError("Please enter your area.")

    def validate_university_other(self, field):
        if self.university.data == "Other" and not (field.data or "").strip():
            raise ValidationError("Please enter your university.")


class EditProfileForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    location = SelectField("Area", choices=with_other(AREA_OPTIONS), validators=[DataRequired()])
    location_other = StringField("Other Area", validators=[Length(max=120)])
    university = SelectField(
        "University", choices=with_other(UNIVERSITY_OPTIONS), validators=[DataRequired()]
    )
    university_other = StringField("Other University", validators=[Length(max=120)])
    submit = SubmitField("Save Changes")

    def validate_location_other(self, field):
        if self.location.data == "Other" and not (field.data or "").strip():
            raise ValidationError("Please enter your area.")

    def validate_university_other(self, field):
        if self.university.data == "Other" and not (field.data or "").strip():
            raise ValidationError("Please enter your university.")
