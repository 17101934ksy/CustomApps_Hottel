from typing import overload
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, HiddenField, DateTimeField
from wtforms.validators import Email, DataRequired, Length, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed

class SiteLoginForm(FlaskForm):
    userName = StringField('아이디',
                         id='user_name_login',
                         validators=[DataRequired()])
    password = PasswordField('비밀번호 (4 ~ 20자 사이)',
                             id='pwd_login',
                             validators=[DataRequired(), Length(min=4, max=20)])

class CreateAccountForm(FlaskForm):
    userName = StringField('아이디',
                         id='user_name_login',
                         validators=[DataRequired()])
    password = PasswordField('비밀번호 (4 ~ 20자 사이)',
                             id='pwd_login',
                             validators=[DataRequired(), Length(min=4, max=20)])
    confirmPassword = PasswordField("비밀번호 확인", 
                            validators=[DataRequired(), EqualTo("password")] )
    email =  StringField("이메일", 
                        id='email',
                        validators=[DataRequired(), Email()])
    phoneNumber = IntegerField('전화번호',
                            id='phone_num',
                            validators=[DataRequired()])

class MagazineForm(FlaskForm):
    visibleTitle = StringField('제목',
                            id='visible-title',
                            validators=[DataRequired("제목을 입력하세요!"), Length(min=2, max=100)])
    hiddenThema = HiddenField('테마',
                            id='hidden-thema')
    hiddenContent = HiddenField('내용',
                            id='hidden-content')
    visibleTag =  StringField('해시태그',
                            id='visible-tag')
    visibleFile = FileField('파일',
                            id='visible-file',
                            validators=[FileAllowed(['jpg', 'png'], 'jpg, png 확장자만 가능합니다.')])


class ReservationForm(FlaskForm):
    period1 = DateTimeField('체크인',
                                id='period_1',
                                validators=[DataRequired("출발일을 선택하세요!")])
    period2 = DateTimeField('체크아웃',
                                id='period_2',
                                validators=[DataRequired("도착일을 선택하세요!")])


class PaymentForm(FlaskForm):


    paymentName = StringField('결제자명',
                                id='payment-name',
                                validators=[DataRequired("결제자 이름을 입력해주세요.")])
    paymentMethod = HiddenField('결제방식',
                                id='payment-method',
                                validators=[DataRequired("결제방식을 선택해주세요.")])
    saleCoupon = HiddenField('할인 쿠폰',
                                id='sale-coupon')
    
    paymentPoint = IntegerField('포인트사용',
                                id='use-point')
    paymentAccount = StringField('계좌번호',
                                id='account',
                                validators=[DataRequired("계좌번호를 입력하세요")])
    paymentRefundAccount = StringField('환불 계좌번호',
                                        id='refund-account',
                                        validators=[DataRequired("환불 계좌를 입력하세요")])
    