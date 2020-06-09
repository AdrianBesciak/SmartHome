from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from system.user import User


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.db.get('username', username.data)
        if user:
            raise ValidationError('This username already exists - choose different one')

    def validate_email(self, email):
        user = User.db.get('email', email.data)
        if user:
            raise ValidationError('This email already exists - choose different one or recover password')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class NewDeviceForm(FlaskForm):
    mode = StringField('mode', validators=[DataRequired()])
    port = StringField('port', validators=[DataRequired()])
    submit = SubmitField('Add device')


class NewScheduleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dev = StringField('Device', validators=[DataRequired()])
    comm = StringField('Service', validators=[DataRequired()])
    mod = StringField('Modifier (at/every)', validators=[DataRequired()])
    unit = StringField('Unit (Available options: minute, hour, day, month, year)', validators=[DataRequired()])
    num = StringField('Interval', validators=[DataRequired()])
    submit = SubmitField('Add task')

    def validate_mod(self, mod):
        if mod not in ['at', 'every']:
            raise ValidationError("Modifier has to be either at or every")

    def validate_unit(self, unit):
        if unit not in ['year', 'month', 'day', 'hour', 'minute']:
            raise ValidationError("Please use a valid unit! Valid units include year, month, day, hour, minute.")


if __name__ == '__main__':
    pass
