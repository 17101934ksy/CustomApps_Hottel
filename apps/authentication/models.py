from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    email = db.Column(db.String(64), unique=True)
    phone_num = db.Column(db.String(64))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.user_name)

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.filter_by(user_id=user_id).first()


@login_manager.request_loader
def request_loader(request):
    user_name = request.form.get('user_name')
    user = Users.query.filter_by(user_name=user_name).first()
    return user if user else None

class Cart(db.Model):
    __tablename__ = 'Cart'

    cart_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64))
    cart_name = db.Column(db.String(200), nullable=False)
    cart_price = db.Column(db.String(100))
    cart_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return str(self.cartname)

class Reservation(db.Model):
    __tablename__ = 'Reservation'

    reserv_seq = db.Column(db.Integer, primary_key=True)
    reserv_time = db.Column(db.DateTime, nullable=False)
    reserv_price = db.Column(db.String(200), nullable=False)
    user_id= db.Column(db.Integer, nullable=False)
    hotel_name = db.Column(db.String(200), nullable=False)
    room_name = db.Column(db.String(200), nullable=False)
    room_time = db.Column(db.DateTime, nullable=False)
    
class BusinessRegistration(db.Model):
    __tablename__ = "BusinessRegistration"

    business_regis_seq = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    business_number = db.Column(db.String(200), unique=True, nullable=False)
    user_addr = db.Column(db.String(200), nullable=False)

# 사업장이 하나가 아닐 수가 있음
class BusinessList(db.Model):
    __tablename__ = "BusinessList"

    business_seq = db.Column(db.Integer, primary_key=True)
    business_addr = db.Column(db.String(200), nullable=False, unique=True)
    user_id = db.Column(db.Integer, nullable=False)

# 주택 타입
class HotelFeature(db.Model):
    __tablename__ = "HotelFeature"

    business_seq = db.Column(db.Integer, primary_key=True)
    room_num = db.Column(db.Integer, primary_key=True, nullable=False)
    hotel_type = db.Column(db.String(100), nullable=False)

class Rooms(db.Model):
    __tablename__ = 'RoomItems'

    room_seq = db.Column(db.Integer, primary_key=True)
    room_reserv_time = db.Column(db.DateTime, nullable=False, primary_key=True)
    room_number = db.Column(db.Integer, nullable=False)
    room_name = db.Column(db.String(200), nullable=False)
    rome_open_time = db.Column(db.DateTime, nullable=False)
    rome_close_time = db.Column(db.DateTime, nullable=False)
    rome_image = db.Column(db.String(300))
    rome_price = db.Column(db.String(100))
    rome_url = db.Column(db.String(200), nullable=False)
    hotel_name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return str(self.hotelname)




