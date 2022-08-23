from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey, ForeignKeyConstraint, Index

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    userId = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(64), nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    phoneNumber = Column(String(64), nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():

            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass(value)
            setattr(self, property, value)

    def __repr__(self):
        return str(self.userName)


class BusinessRegisters(db.Model):

    __tablename__ = "BusinessRegisters"

    businessRegisId = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    businessNumber = Column(String(200), unique=True, nullable=False)

    users = db.relationship('Users', backref='BusinessRegisters')


class BusinessLists(db.Model):

    __tablename__ = "BusinessLists"

    businessId = Column(Integer, primary_key=True)
    businessAddr = Column(String(200), nullable=False, unique=True)
    userId = Column(Integer, ForeignKey('Users.userId'))

    user = db.relationship('Users', backref='BusinessLists')

class Accomodations(db.Model):

    __tablename__ = "Accomodations"

    accomodationId = Column(Integer, ForeignKey('BusinessLists.businessId'), primary_key=True)
    accomodationType = Column(String(100), nullable=False)
    accomodationName = Column(String(100), nullable=False)
    accomodationUrl = Column(String(100), nullable=False)

    businessLists = db.relationship('BusinessLists', backref='Accomodations')

   
class Rooms(db.Model):

    __tablename__ = 'Rooms'

    roomId = Column(Integer, primary_key=True, autoincrement=True)
    roomDateTime = Column(DateTime, nullable=False)
    roomNumber = Column(Integer, nullable=False)
    roomName = Column(String(200), nullable=False)
    romeCheckIn = Column(DateTime, nullable=False)
    romeCheckOut = Column(DateTime, nullable=False)
    romeImage = Column(String(300))
    romePrice = Column(String(100))
    romeUrl = Column(String(200), nullable=False)
    accomodationId = Column(Integer, ForeignKey('Accomodations.accomodationId'))

    accomodations = db.relationship('Accomodations', backref='Rooms')


class Carts(db.Model):

    __tablename__ = 'Carts'

    cartId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    roomId = Column(Integer, ForeignKey('Rooms.roomId'))

    users = db.relationship('Users', backref='Carts')
    rooms = db.relationship('Rooms', backref='Carts')
    
class Reservations(db.Model):
    
    __tablename__ = 'Reservations'

    reserveId = Column(Integer, primary_key=True, autoincrement=True)
    reserveTime = Column(DateTime, nullable=False)
    reservePrice = Column(String(200), nullable=False)
    cartId = Column(Integer, ForeignKey('Carts.cartId'))

    carts = db.relationship('Carts', backref='Reservations')


@login_manager.user_loader
def user_loader(userId):
    return Users.query.filter_by(useId=userId).first()


@login_manager.request_loader
def request_loader(request):
    userName = request.form.get('userName')
    user = Users.query.filter_by(userName=userName).first()
    return user if user else None