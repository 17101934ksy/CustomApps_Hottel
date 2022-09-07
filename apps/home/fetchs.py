from apps.authentication.models import Accomodations, Reservations, SaleCoupons, Testimonials, Users, Magazines, Rooms
from datetime import datetime, date
from sqlalchemy import and_, or_

"""
databases에서 데이터를 가져오는 func
"""

def fetch_accomodations(number):

    accomodations = Accomodations.query.order_by(Accomodations.accomodationId.desc()).limit(number).all()
    ids, names, images, prices = [], [], [], []

    for accomodation in accomodations:
        ids.append(accomodation.accomodationId)
        names.append(accomodation.accomodationName)
        images.append(accomodation.accomodationImage)
        prices.append(accomodation.accomodationPrice)
    
    return ids, names, images, prices

def fetch_testimonials(number):

    testimonials = Testimonials.query.order_by(Testimonials.testimonialId.desc()).limit(number).all()
    ids, names, comments = [], [], []

    for testimonial in testimonials:
        users = Users.query.filter_by(userId=testimonial.userId).first()
        ids.append(users.userId)
        names.append(users.userName)
        comments.append(testimonial.testimonialComment)

    return ids, names, comments

def fetch_magazines(number):

    if number == 'all':
        magazines = Magazines.query.order_by(Magazines.magazineView.desc()).all()
    else:
        magazines = Magazines.query.order_by(Magazines.magazineView.desc()).limit(number).all()

    magazines = convert_dict(magazines)
    
    return magazines




def fetch_magazines_detail(magazine, number):
    return magazine[number]



def fetch_rooms(accomodation_id):
    rooms = Rooms.query.filter_by(accomodationId=accomodation_id).all()
    rooms = convert_dict(rooms)

    return rooms


def fetch_room_details(room_id):
    room = Rooms.query.filter_by(roomId=room_id).first()
    reservations = Reservations.query.filter(and_(Reservations.roomId==room_id, date.today() < Reservations.roomCheckOutDate)).all()

    if reservations is not None:

        reservation = {'roomCheckInDate': [], 'roomCheckOutDate': []}
        for dt in reservations:
            reservation['roomCheckInDate'].append(dt.roomCheckInDate)
            reservation['roomCheckOutDate'].append(dt.roomCheckOutDate)

    return room, reservation


def fetch_user_coupon(user_coupon, room):

    coupons = []

    for cou in user_coupon:
        coupon = SaleCoupons.query.filter_by(saleCouponId=cou.couponId).first()

        if coupon.accmodationTypeConstraint is None and coupon.accmodationIdConstraint is None:
            coupons.append(coupon)
        
        elif coupon.accmodationTypeConstraint is not None and coupon.accmodationIdConstraint is None:
            return 1

    
    return "사용 가능한 쿠폰이 없습니다."


def convert_dict(db_item):

    item_data = {}

    for key in db_item[0].__dict__.keys():
        item_data[key] = []
    
    for item in db_item:
        for key, value in zip([item_data[k] for k in item_data.keys()], item.__dict__.values()):
            key.append(value)

    return item_data

