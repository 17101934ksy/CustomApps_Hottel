# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, IntegerField, FloatField
# from wtforms.validators import Email, DataRequired

# # login and registration


# class LoginForm(FlaskForm):
#     username = StringField('Username',
#                          id='username_login',
#                          validators=[DataRequired()])
#     password = PasswordField('Password',
#                              id='pwd_login',
#                              validators=[DataRequired()])


# class CreateAccountForm(FlaskForm):
#     username = StringField('Username',
#                          id='username_create',
#                          validators=[DataRequired()])
#     email = StringField('Email',
#                       id='email_create',
#                       validators=[DataRequired(), Email()])
#     password = PasswordField('Password',
#                              id='pwd_create',
#                              validators=[DataRequired()])


# class CreateTypeForm(FlaskForm):
#     hectare = StringField('Hectare',
#                          id='hectare_create',
#                          validators=[DataRequired()])
                         
#     qaulity = StringField('Quality',
#                       id='quality_create',
#                       validators=[DataRequired()])

#     departure = StringField('Departure',
#                              id='departure_create',
#                              validators=[DataRequired()])

#     destination = StringField('Destination',
#                              id='destination_create',
#                              validators=[DataRequired()])

#     fiveton =  IntegerField('FiveTon',
#                             id='fiveton_create',
#                             validate=[DataRequired()])

#     twentyfiveton = IntegerField('TwentyFiveTon',
#                                 id='fiveton_create',
#                                 validate=[DataRequired()])

#     email = StringField('Email',
#                       id='email_create',
#                       validators=[DataRequired(), Email()])         