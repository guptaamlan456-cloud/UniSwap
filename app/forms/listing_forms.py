from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    BooleanField,
    DateField,
    DecimalField,
    MultipleFileField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.validators import ValidationError

from app.constants.options import AREA_OPTIONS, UNIVERSITY_OPTIONS, with_other
from app.utils.image_upload import upload_image_file


class ListingForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=2000)])
    price = DecimalField("Price (RM)", validators=[NumberRange(min=0)], default=0)
    category = SelectField(
        "Category",
        choices=[
            ("Furniture", "Furniture"),
            ("Electronics", "Electronics"),
            ("Textbooks", "Textbooks"),
            ("Clothing", "Clothing"),
            ("Other", "Other"),
        ],
        validators=[DataRequired()],
    )
    condition = SelectField(
        "Condition",
        choices=[
            ("New", "New"),
            ("Like New", "Like New"),
            ("Good", "Good"),
            ("Fair", "Fair"),
        ],
        validators=[DataRequired()],
    )
    location = SelectField("Area", choices=with_other(AREA_OPTIONS), validators=[DataRequired()])
    location_other = StringField("Other Area", validators=[Length(max=120)])
    university = SelectField(
        "University", choices=with_other(UNIVERSITY_OPTIONS), validators=[DataRequired()]
    )
    university_other = StringField("Other University", validators=[Length(max=120)])
    urgency_level = SelectField(
        "Urgency",
        choices=[
            ("very_urgent", "Very urgent"),
            ("medium", "Medium urgency"),
            ("low", "Low urgency"),
        ],
        validators=[DataRequired()],
    )
    departure_date = DateField("Departure Date", validators=[DataRequired()], format="%Y-%m-%d")
    free = BooleanField("Free Giveaway")
    clear_images = BooleanField("Remove all existing images")
    images = MultipleFileField(
        "Upload Images",
        validators=[FileAllowed(["jpg", "jpeg", "png", "webp", "gif"], "Images only!")],
    )
    submit = SubmitField("Create Listing")

    def validate_location_other(self, field):
        if self.location.data == "Other" and not (field.data or "").strip():
            raise ValidationError("Please enter area if not listed.")

    def validate_university_other(self, field):
        if self.university.data == "Other" and not (field.data or "").strip():
            raise ValidationError("Please enter university if not listed.")

    def upload_images(self):
        uploaded = []
        if not self.images.data:
            return uploaded
        for file_obj in self.images.data:
            if not file_obj:
                continue
            result = upload_image_file(file_obj, folder="uniswap/listings")
            if result and result.get("secure_url"):
                uploaded.append(result.get("secure_url"))
        return uploaded
