from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, BooleanField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField

class FormRegister(FlaskForm):
    """依照Model來建置相對應的Form

    password2: 用來確認兩次的密碼輸入相同
    """
    username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(2, 30, message='Length of password must between %(min)d and %(max)d')
    ])

    nickname = StringField('Nickname', validators=[
        validators.DataRequired(),
        validators.Length(1, 30)
    ])

    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(6, 20, message='Length of password must between %(min)d and %(max)d'),
        validators.EqualTo('confirm', message='password must be as same as the comfirm password')
    ])
    confirm = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Register New Account')


class FormLogin(FlaskForm):
    """
    使用者登入使用
    以email為主要登入帳號，密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """

    username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(2, 30)
    ])

    password = PasswordField('PassWord', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('Keep Logged in')

    submit = SubmitField('Log in')


class FormEdit(FlaskForm):
    """
    """

    username = StringField('UserName')

    nickname = StringField('Nickname', validators=[
        validators.Optional(),
        validators.Length(1, 30)
    ])

    email = EmailField('Email', validators=[
        validators.Optional(),
        validators.Length(1, 50, 'Length of email must between %(min)d and %(max)d'),
        validators.Email()
    ])
    current_password = PasswordField('CurrentPassWord', validators=[
        validators.DataRequired(),
        validators.Length(2, 10, 'Length of current password must between %(min)d and %(max)d')
    ])
    password = PasswordField('PassWord', validators=[
        validators.Optional(),
        validators.Length(2, 10, 'Length of new password must between %(min)d and %(max)d'),
        validators.EqualTo('confirm', message='New password must be as same as the comfirm password')
    ])
    confirm = PasswordField('Confirm PassWord', validators=[
        validators.Optional(),
    ])
    submit = SubmitField('Edit Your Profile')


class FormAnnounce(FlaskForm):
    """
    """

    title = StringField('Title', validators = [
        validators.DataRequired(),
        validators.Length(1, 100)
    ])

    content = TextAreaField('Announce', validators=[
        validators.DataRequired()
    ])

    submit = SubmitField('submit')