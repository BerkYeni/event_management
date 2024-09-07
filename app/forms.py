from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import Attendee
from datetime import datetime

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeField('Date and Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create Event')

    def validate_date(self, field):
        if field.data < datetime.now():
            raise ValidationError('Event date must be in the future')

class AttendeeRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        attendee = Attendee.query.filter_by(email=email.data).first()
        if attendee:
            raise ValidationError('This email is already registered. Please use a different email.')

class AttendeeManagementForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
