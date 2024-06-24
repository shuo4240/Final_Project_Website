from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms.fields import EmailField
from wtforms import BooleanField
from app.model import UserRegister


class FormRegister(FlaskForm):
    """依照Model來建置相對應的Form

    password2: 用來確認兩次的密碼輸入相同
    """
    username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(10, 30)
    ])
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ])
    password2 = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if UserRegister.query.filter_by(email=email.data).first():
            raise validators.ValidationError('Email already register by somebody')

    def validate_username(self, field):
        if UserRegister.query.filter_by(username=field.data).first():
            raise validators.ValidationError('UserName already register by somebody')


class FormLogin(FlaskForm):
    """
    使用者登入使用
    以email為主要登入帳號，密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """

    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])

    password = PasswordField('PassWord', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('Keep Logged in')

    submit = SubmitField('Log in')

class UsernameUpdate(FlaskForm):
    new_username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(10, 30)
    ])
    submit = SubmitField('Updates')

class PasswordUpdate(FlaskForm):
    current_password = PasswordField('Current PassWord', validators=[
        validators.DataRequired()
    ])
    new_password = PasswordField('New PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('new_password2', message='PASSWORD NEED MATCH')
    ])
    new_password2 = PasswordField('Confirm New PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Update')
