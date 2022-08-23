from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField
from wtforms.validators import Email, DataRequired, Length, EqualTo

# login and registration


class SiteLoginForm(FlaskForm):
    user_name = StringField('아이디',
                         id='user_name_login',
                         validators=[DataRequired()])
    password = PasswordField('비밀번호 (4 ~ 20자 사이)',
                             id='pwd_login',
                             validators=[DataRequired(), Length(min=4, max=20)])


class CreateAccountForm(FlaskForm):
    user_name = StringField('아이디',
                         id='user_name_login',
                         validators=[DataRequired()])
    password = PasswordField('비밀번호 (4 ~ 20자 사이)',
                             id='pwd_login',
                             validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField("비밀번호 확인", 
                            validators=[DataRequired(), EqualTo("password")] )
    email =  StringField("이메일", 
                        id='email',
                        validators=[DataRequired(), Email()])
    phone_num = IntegerField('전화번호',
                            id='phone_num',
                            validators=[DataRequired()])
