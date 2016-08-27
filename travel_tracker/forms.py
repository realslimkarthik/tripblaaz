from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms import validators
from travel_tracker.models import User

from flask_security.forms import RegisterForm

class ExtendedRegisterForm(RegisterForm):
    recaptcha = RecaptchaField()
    accept_tos = BooleanField('I accept the Terms & Conditions', [validators.DataRequired()])
