from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, EmailField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from .models import UsersModel

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UserRegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=32)])
    email = EmailField('E-mail', validators=[Email(), DataRequired()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=32)])
    password_2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    gender = SelectField('Gender', choices=['male', 'female'], validators=[DataRequired()])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = UsersModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = UsersModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140), DataRequired()])
    submit = SubmitField('Submit')



class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

