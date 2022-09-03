from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey, Float, TEXT, DATE, BOOLEAN

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
    roomNumber = Column(Integer, nullable=False)
    roomName = Column(String(200), nullable=False)
    roomCheckIn = Column(String(100), nullable=False)
    roomCheckOut = Column(String(100), nullable=False)
    roomStandardPopulation =Column(Integer)
    roomUptoPopulation =Column(Integer)
    roomImage = Column(String(300))
    roomWifi = Column(BOOLEAN)
    roomAirConditioner = Column(BOOLEAN)
    roomMicrowave = Column(BOOLEAN)
    roomTv = Column(BOOLEAN)
    roomRate = Column(Float, nullable=True)
    roomSalePrice = Column(Integer, nullable=True)
    roomOriginalPrice = Column(Integer, nullable=False)
    accomodationId = Column(Integer, ForeignKey('Accomodations.accomodationId'))

    accomodations = db.relationship('Accomodations', backref='Rooms')

    def __repr__(self):
        self.info = {
            "roomId": self.roomId,
            "roomNumber": self.roomNumber,
            "roomName": self.roomName,
            "roomCheckIn": self.roomCheckIn,
            "roomCheckOut": self.roomCheckOut,
            "roomStandardPopulation": self.roomStandardPopulation,
            "roomUptoPopulation": self.roomUptoPopulation,
            "roomImage": self.roomImage,
            "roomWifi": self.roomWifi,
            "roomAirConditioner": self.roomAirConditioner,
            "roomMicrowave": self.roomMicrowave,
            "roomTv": self.roomTv,
            "roomRate": self.roomRate,
            "roomSalePrice": self.roomSalePrice,
            "roomOriginalPrice": self.roomOriginalPrice,
            "accomodationId": self.accomodationId
        }
        return str(self.info) 

class RoomDateTimes(db.Model):

    __tablename__ = 'RoomDateTimes'

    roomSeq = Column(Integer, primary_key=True, autoincrement=True)
    roomId = Column(Integer, ForeignKey('Rooms.roomId'))
    roomDateTime = Column(DATE, nullable=False)
    roomDynamicPrice = Column(Integer, nullable=True)
    
    rooms = db.relationship('Rooms', backref='RoomDateTimes')

    def __repr__(self):
        self.info = {
            "roomSeq": self.roomSeq,
            "roomId": self.roomId,
            "roomDateTime": self.roomDateTime,
            "roomDynamicPrice": self.roomDynamicPrice
        }
        return str(self.info) 


class Carts(db.Model):

    __tablename__ = 'Carts'

    cartId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    roomSeq = Column(Integer, ForeignKey('RoomDateTimes.roomSeq'))

    users = db.relationship('Users', backref='Carts')
    roomDateTimes = db.relationship('RoomDateTimes', backref='Carts')

    def __repr__(self):
        self.info = {
            "cartId": self.cartId,
            "userId": self.userId,
            "roomSeq": self.roomSeq
        }
        return str(self.info)


    
class Reservations(db.Model):
    
    __tablename__ = 'Reservations'

    reserveSeq = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'), nullable=False)
    roomSeq = Column(Integer, ForeignKey('RoomDateTimes.roomSeq'), nullable=False)
    paymentMethodSeq = Column(Integer, ForeignKey('PaymentMethods.paymentMethodSeq'), nullable=False) 
    paymentSaleId = Column(Integer, ForeignKey('PaymentSaleMethods.paymentSaleId'),nullable=True)

    paymentDateTime = Column(DateTime, nullable=False)
    paymentName = Column(String(200), nullable=False)
    paymentPoint = Column(Integer, nullable=False)
    paymentAccount = Column(String(300), nullable=True)
    paymentRefundAccount = Column(String(300), nullable=False)

    users = db.relationship('Users', backref='Reservations')
    roomDateTimes = db.relationship('RoomDateTimes', backref='Reservations')
    paymentMethods = db.relationship('PaymentMethods', backref='Reservations')
    paymentSaleMethods = db.relationship('PaymentSaleMethods', backref='Reservations') 

    def __repr__(self):
        self.info = {
            "reserveSeq": self.reserveSeq,
            "userId": self.userId,
            "roomSeq": self.roomSeq,
            "paymentMethodSeq": self.paymentMethodSeq,
            "paymentSaleId": self.paymentSaleId,
            "paymentDateTime": self.paymentDateTime,
            "paymentName": self.paymentName,
            "paymentPoint": self.paymentPoint,
            "paymentAccount": self.paymentAccount,
            "paymentRefundAccount": self.paymentRefundAccount
        }
        return str(self.info)

class PaymentSaleMethods(db.Model):

    __tablename__ = "PaymentSaleMethods"

    paymentSaleId = Column(Integer, primary_key=True, autoincrement=True)
    paymentSaleMethod = Column(String(400), nullable=False)
    paymentSalePrice = Column(Integer, nullable=True)
    paymentSaleRate = Column(Float, nullable=True)

    def __repr__(self):
        self.info = {
            "paymentSaleId": self.paymentSaleId,
            "paymentSaleMethod": self.paymentSaleMethod,
            "paymentSalePrice": self.paymentSalePrice,
            "paymentSaleRate": self.paymentSaleRate
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


class RoomReviews(db.Model):
    
    __tablename__ = 'RoomReviews'

    roomReviewSeq = Column(Integer, primary_key=True, autoincrement=True)
    completeSeq = Column(Integer, ForeignKey('UsedCompletes.completeSeq'))

    reviewImage1 = Column(String(400), nullable=True)
    reviewImage2 = Column(String(400), nullable=True)
    reviewImage3 = Column(String(400), nullable=True)
    reviewComment = Column(String(1000), nullable=False)

    usedCompletes = db.relationship('UsedCompletes', backref='RoomReviews')

    def __repr__(self):
        self.info = {
            "roomReviewId": self.roomReviewId,
            "completeSeq": self.completeSeq,
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

class RoomReviewComments(db.Model):

    __tablename__ = 'RoomReviewComments'

    reviewCommentSeq = Column(Integer, primary_key=True, autoincrement=True)
    roomReviewSeq = Column(Integer, ForeignKey('RoomReviews.roomReviewSeq'), primary_key=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    reviewComment = Column(TEXT, nullable=False)

    roomReviews = db.relationship('RoomReviews', backref='RoomReviewComments')
    users = db.relationship('Users', backref='RoomReviewComments')

    def __repr__(self):
        self.info = {
            "reviewCommentSeq": self.reviewCommentSeq,
            "roomReviewSeq": self.roomReviewSeq,
            "userId": self.userId,
            "reviewComment": self.reviewComment
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

    magazineCommentSeq = Column(Integer, primary_key=True, autoincrement=True)
    magazineSeq = Column(Integer, ForeignKey('Magazines.magazineSeq'))
    userId = Column(Integer, ForeignKey('Users.userId'))
    magazineComment = Column(TEXT)

    users = db.relationship('Users', backref='MagazineComments')
    magazines = db.relationship('Magazines', backref='MagazineComments')
    
    def __repr__(self):
        self.info = {
                "magazineCommentSeq": self.magazineCommentSeq,
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

class UsedCompletes(db.Model):

    __tablename__ = 'UsedCompletes'

    completeSeq = Column(Integer, primary_key=True, autoincrement=True)
    reserveSeq = Column(Integer, ForeignKey('Reservations.reserveSeq')) 

    def __repr__(self):
        self.info = {
            "completeSeq": self.completeSeq,
            "reserveSeq": self.reserveSeq,
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