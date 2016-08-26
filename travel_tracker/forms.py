from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms import validators
from travel_tracker.models import User



class LoginForm(Form):
    username = StringField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.optional()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # Does our the exist
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False

        return True


class RegisterForm(Form):
    username = StringField(u'Username', validators=[validators.required()])
    password = PasswordField(u'New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField(u'Confirm Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')])
    email = StringField(u'Email', validators=[validators.DataRequired(), validators.Email()])
    first_name = StringField(u'First Name', validators=[validators.required()])
    last_name = StringField(u'Last Name', validators=[validators.required()])
    recaptcha = RecaptchaField()
    accept_tos = BooleanField('I accept the Terms & Conditions', [validators.DataRequired()])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already exists. Click <a href='{{ url_for(\'.forgot_password\') }}'>here</a> if you forgot password.")
            return False

        email = User.query.filter_by(email=self.email.data).first()
        if email:
            self.email.errors.append("Email already exists. Click <a href='{{ url_for(\'.forgot_password\') }}'>here</a> if you forgot password.")
            return False

        return True
