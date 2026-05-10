from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ChatMessageForm(FlaskForm):
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Send")


class OfferActionForm(FlaskForm):
    submit = SubmitField("Confirm")
