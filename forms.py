from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=7, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please login.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RepairBookingForm(FlaskForm):
    brand = SelectField('Mobile Brand', choices=[
        ('Apple', 'Apple'), ('Samsung', 'Samsung'), ('OnePlus', 'OnePlus'),
        ('Xiaomi', 'Xiaomi'), ('Oppo', 'Oppo'), ('Vivo', 'Vivo'),
        ('Google', 'Google'), ('Motorola', 'Motorola'), ('Realme', 'Realme'),
        ('Nothing', 'Nothing'), ('Other', 'Other')
    ], validators=[DataRequired()])
    model = StringField('Phone Model', validators=[DataRequired(), Length(max=100)])
    problem = TextAreaField('Problem Description', validators=[DataRequired(), Length(max=1000)])
    image = FileField('Upload Image (optional)', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    pickup_address = TextAreaField('Pickup Address', validators=[DataRequired(), Length(max=300)])
    pickup_date = DateField('Preferred Pickup Date', validators=[DataRequired()])
    pickup_time_slot = SelectField('Time Slot', choices=[
        ('9AM-11AM', '9:00 AM – 11:00 AM'),
        ('11AM-1PM', '11:00 AM – 1:00 PM'),
        ('2PM-4PM', '2:00 PM – 4:00 PM'),
        ('4PM-6PM', '4:00 PM – 6:00 PM'),
    ], validators=[DataRequired()])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(min=7, max=20)])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Book Repair')

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Update Profile')

class AdminRepairUpdateForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('Requested', 'Requested'), ('Picked Up', 'Picked Up'),
        ('Under Repair', 'Under Repair'), ('Ready', 'Ready'), ('Delivered', 'Delivered')
    ], validators=[DataRequired()])
    repair_cost = FloatField('Repair Cost (₹)', validators=[Optional()])
    admin_notes = TextAreaField('Internal Notes', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Update')
