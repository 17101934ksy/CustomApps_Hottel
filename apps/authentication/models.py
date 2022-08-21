from flask_login import UserMixin

# from apps import db, login_manager

# from apps.authentication.util import hash_pass

# class Users(db.Model, UserMixin):

#     __tablename__ = 'Users'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True)
#     email = db.Column(db.String(64), unique=True)
#     password = db.Column(db.LargeBinary)

#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]

#             if property == 'password':
#                 value = hash_pass(value)  # we need bytes here (not plain str)

#             setattr(self, property, value)

#     def __repr__(self):
#         return str(self.username)


# class Prices(db.Model, UserMixin):

#     __tablename__ = 'Prices'

#     email = db.Column(db.String(64), primary_key=True, unique=True)
#     hectare = db.Column(db.Float)
#     special_goods = db.Column(db.Integer)
#     first_goods = db.Column(db.Integer)
#     second_goods = db.Column(db.Integer)
#     third_goods = db.Column(db.Integer)
#     original_goods = db.Column(db.Integer)
#     raw_goods = db.Column(db.Integer)
#     departure = db.Column(db.String(100))
#     destination = db.Column(db.String(100))
#     fiveton = db.Column(db.Integer)
#     twentyfiveton = db.Column(db.Integer)

#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]

#             setattr(self, property, value)

#     def __repr__(self):
#         return str(self.email)


# @login_manager.user_loader
# def user_loader(id):
#     return Users.query.filter_by(id=id).first()


# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     user = Users.query.filter_by(username=username).first()
#     return user if user else None