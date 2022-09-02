from sqlite3 import Date
from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey, Float, TEXT, DATE

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

    def get_id(self):
        return (self.userId)

    def __repr__(self):
        self.info = {
            "userId": self.userId,
            "userName": self.userName,
            "email": self.email,
            "phoneNumber": self.phoneNumber
        }
        return str(self.info)


class BusinessRegisters(db.Model):

    __tablename__ = "BusinessRegisters"

    businessRegisId = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    businessNumber = Column(String(200), unique=True, nullable=False)
    users = db.relationship('Users', backref='BusinessRegisters')

    def __repr__(self):
        self.info = {
            "businessRegisId": self.businessRegisId,
            "userId": self.userId,
            "businessNumber": self.businessNumber
        }
        return str(self.info)


class BusinessLists(db.Model):

    __tablename__ = "BusinessLists"

    businessId = Column(Integer, primary_key=True)
    businessAddr = Column(String(200), nullable=False, unique=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    user = db.relationship('Users', backref='BusinessLists')

    def __repr__(self):
        self.info = {
            "businessId": self.businessId,
            "businessAddr": self.businessAddr,
            "userId": self.userId
        }
        return str(self.info)

class Accomodations(db.Model):

    __tablename__ = "Accomodations"

    accomodationId = Column(Integer, ForeignKey('BusinessLists.businessId'), primary_key=True)
    accomodationType = Column(String(100), nullable=False)
    accomodationName = Column(String(100), nullable=False)
    accomodationImage = Column(String(300))
    accomodationPrice = Column(String(200))

    businessLists = db.relationship('BusinessLists', backref='Accomodations')

    def __repr__(self):
        self.info = {
            "accomodationId": self.accomodationId,
            "accomodationType": self.accomodationType,
            "accomodationName": self.accomodationName,
            "accomodationImage": self.accomodationImage,
            "accomodationPrice": self.accomodationPrice,
        }
        return str(self.info)
   
class Rooms(db.Model):

    __tablename__ = 'Rooms'

    roomId = Column(Integer, primary_key=True, autoincrement=True)
    roomDateTime = Column(DATE, nullable=False)
    roomNumber = Column(Integer, nullable=False)
    roomName = Column(String(200), nullable=False)
    roomCheckIn = Column(DateTime, nullable=False)
    roomCheckOut = Column(DateTime, nullable=False)
    roomStandardPopulation =Column(Integer)
    roomUptoPopulation =Column(Integer)
    roomImage = Column(String(300))
    roomSalePrice = Column(String(100), nullable=True)
    roomOriginalPrice = Column(String(100))
    roomRate = Column(Float, nullable=True)
    accomodationId = Column(Integer, ForeignKey('Accomodations.accomodationId'))

    accomodations = db.relationship('Accomodations', backref='Rooms')

    def __repr__(self):
        self.info = {
            "roomId": self.roomId,
            "roomDateTime": self.roomDateTime,
            "roomNumber": self.roomNumber,
            "roomName": self.roomName,
            "romeCheckIn": self.roomCheckIn,
            "romeCheckOut": self.roomCheckOut,
            "roomStandardPopulation": self.roomStandardPopulation,
            "roomUptoPopulation": self.roomUptoPopulation,
            "romeImage": self.roomImage,
            "roomSalePrice": self.roomSalePrice,
            "romeOriginalPrice": self.roomOriginalPrice,
            "roomRate": self.roomRate,
            "accomodationId": self.accomodationId
        }
        return str(self.info) 

class Carts(db.Model):

    __tablename__ = 'Carts'

    cartId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    roomId = Column(Integer, ForeignKey('Rooms.roomId'))

    users = db.relationship('Users', backref='Carts')
    rooms = db.relationship('Rooms', backref='Carts')

    def __repr__(self):
        self.info = {
            "cartId": self.cartId,
            "userId": self.userId,
            "roomId": self.roomId
        }
        return str(self.info)
    
class Reservations(db.Model):
    
    __tablename__ = 'Reservations'

    reserveId = Column(Integer, primary_key=True, autoincrement=True)
    reserveTime = Column(DateTime, nullable=False)
    reservePrice = Column(String(200), nullable=False)
    cartId = Column(Integer, ForeignKey('Carts.cartId'))

    carts = db.relationship('Carts', backref='Reservations')

    def __repr__(self):
        self.info = {
            "reserveId": self.reserveId,
            "reserveTime": self.reserveTime,
            "reservePrice": self.reservePrice,
            "cartId": self.cartId
        }
        return str(self.info) 


class Testimonials(db.Model):

    __tablename__ = 'Testimonials'

    testimonialId = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    testimonialComment = Column(String(1000), nullable=False)

    users = db.relationship('Users', backref='Testimonials')

    def __repr__(self):
        self.info = {
            "testimonialId": self.testimonialId,
            "userId": self.userId,
            "testimonialComment": self.testimonialComment,
        }
        return str(self.info) 


class Reviews(db.Model):
    
    __tablename__ = 'Reviews'

    reviewId = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    reserveId = Column(Integer, ForeignKey('Reservations.reserveId'))

    reviewImage1 = Column(String(400), nullable=True)
    reviewImage2 = Column(String(400), nullable=True)
    reviewImage3 = Column(String(400), nullable=True)
    reviewComment = Column(String(1000), nullable=False)

    users = db.relationship('Users', backref='Reviews')
    reserves = db.relationship('Reservations', backref='Reviews')

    def __repr__(self):
        self.info = {
            "reviewId": self.reviewId,
            "userId": self.userId,
            "reserveId": self.reserveId,
            "reviewImage1": self.reviewImage1,
            "reviewImage2": self.reviewImage2,
            "reviewImage3": self.reviewImage3,
            "reviewComment": self.reviewComment,
        }
        return str(self.info) 

class Points(db.Model):

    __tablename__ = 'Points'

    userId = Column(Integer, ForeignKey('Users.userId'), primary_key=True)
    pointSum = Column(Integer)

    users = db.relationship('Users', backref='Points')

    def __repr__(self):
        self.info = {
            "userId": self.userId,
            "pointSum": self.pointSum,
        }
        return str(self.info) 

class ReviewComments(db.Model):

    __tablename__ = 'ReviewComments'

    reviewId = Column(Integer, ForeignKey('Reviews.reviewId'), primary_key=True)
    commentSeq = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    commentContent = Column(TEXT, nullable=False)

    reviews = db.relationship('Reviews', backref='ReviewComments')
    users = db.relationship('Users', backref='ReviewComments')

    def __repr__(self):
        self.info = {
            "reviewId": self.userId,
            "commentSeq": self.commentSeq,
            "userId": self.userId,
            "commentContent": self.commentContent
        }
        return str(self.info) 
    

class Magazines(db.Model):

    __tablename__ = 'Magazines'

    magazineSeq = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    magazineThema = Column(String(200), nullable=False)
    magazineWriter = Column(String(400), nullable=False)
    magazineDate = Column(DateTime, nullable=False)
    magazineView = Column(Integer, nullable=False)
    magazineTitle = Column(String(400), nullable=False)
    magazineSubTitle = Column(String(400), nullable=True)
    magazineContent = Column(TEXT, nullable=False)
    magazineLink= Column(String(700), nullable=False)
    magazineTag= Column(String(800), nullable=False)
    magazineImage = Column(String(1000), nullable=True)

    users = db.relationship('Users', backref='Magazines')

    def __repr__(self):
        self.info = {
            "magazineSeq": self.magazineSeq,
            "userId": self.userId,
            "magazineThema": self.magazineThema,
            "magazineWriter": self.magazineWriter,
            "magazineDate": self.magazineDate,
            "magazineView": self.magazineView,
            "magazineTitle": self.magazineTitle,
            "magazineSubTitle": self.magazineSubTitle,
            "magazineContent": self.magazineContent,
            "magazineLink": self.magazineLink,
            "magazineTag": self.magazineTag,
            "magazineImage": self.magazineImage
        }
        return str(self.info) 

class MagazineComments(db.Model):

    __tablename__ = 'MagazineComments'

    commentSeq = Column(Integer, primary_key=True, autoincrement=True)
    magazineSeq = Column(Integer, ForeignKey('Magazines.magazineSeq'))
    userId = Column(Integer, ForeignKey('Users.userId'))
    magazineComment = Column(TEXT)

    users = db.relationship('Users', backref='MagazineComments')
    magazines = db.relationship('Magazines', backref='MagazineComments')
    
    def __repr__(self):
        self.info = {
                "commentSeq": self.commentSeq,
                "magazineSeq": self.magazineSeq,
                "userId": self.userId,
                "magazineComment": self.magazineComment
            }
        return str(self.info)


class PaymentMethods(db.Model):
    
    __tablename__ = 'PaymentMethods'

    paymentMethodSeq = Column(Integer, primary_key=True, autoincrement=True)
    paymentMethod = Column(String(300), nullable=False)
    paymentDepositAccount = Column(String(300), nullable=True)

    def __repr__(self):
        self.info = {
            "paymentMethodSeq": self.paymentMethodSeq,
            "paymentMethod": self.paymentMethod,
            "paymentDepositAccount": self.paymentDepositAccount
        }
        return self.info

class CompleteReservations(db.Model):

    __tablename__ = 'CompleteReservations'

    completeSeq = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'), nullable=False)
    roomId = Column(Integer, ForeignKey('Rooms.roomId'), nullable=False)
    paymentMethodSeq = Column(Integer, ForeignKey('PaymentMethods.paymentMethodSeq'), nullable=False) 

    paymentDateTime = Column(DateTime, nullable=False)
    paymentName = Column(String(200), nullable=False)
    paymentPoint = Column(Float, nullable=False)
    paymentSale = Column(Integer, nullable=False)
    paymentPrice = Column(Float, nullable=False)
    paymentAccount = Column(String(300), nullable=True)
    paymentRefundAccount = Column(String(300), nullable=False)

    users = db.relationship('Users', backref='CompleteReservations')
    rooms = db.relationship('Rooms', backref='CompleteReservations')
    paymentMethods = db.relationship('PaymentMethods', backref='CompleteReservations')

    def __repr__(self):
        self.info = {
            "completeSeq": self.completeSeq,
            "userId": self.userId,
            "roomId": self.roomId,
            "paymentDateTime": self.paymentDateTime,
            "paymentMethodSeq": self.paymentMethodSeq,
            "paymentName": self.paymentName,
            "paymentPoint": self.paymentPoint,
            "paymentSale": self.paymentSale,
            "paymentPrice": self.paymentPrice,
            "paymentAccount": self.paymentAccount,
            "paymentRefundAccount": self.paymentRefundAccount
        }
        return str(self.info)



@login_manager.user_loader
def user_loader(userId):
    return Users.query.filter_by(userId=userId).first()


@login_manager.request_loader
def request_loader(request):
    userName = request.form.get('userName')
    user = Users.query.filter_by(userName=userName).first()
    return user if user else None