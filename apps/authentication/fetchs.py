from apps.authentication.models import Accomodations, Reservations, Testimonials, Users, Magazines, Rooms, RoomDateTimes
from datetime import datetime, date
from sqlalchemy import and_
from calendar import monthrange

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


def fetch_room_details(room_id, select_time=date.today()):
    room = Rooms.query.filter_by(roomId=room_id).first()

    room_datetimes = RoomDateTimes.query.join(RoomDateTimes.Reservations).filter(and_(select_time<=RoomDateTimes.roomDateTime, RoomDateTimes.roomId==room_id)).limit(60).all()

    print(room_datetimes)
    reservation_able = []

    for room_datetime in room_datetimes:
        reservation = Reservations.query.filter_by(roomSeq=room_datetime.roomSeq)

        if reservation is not None:
            continue
        reservation_able.append(reservation)
    
    # reservation_data = convert_dict(reservation_able)

    # return reservation_able

    # reservation = Reservations.query.filter_by(roomId=room_id).all()
    return room



def convert_dict(db_item):

    item_data = {}

    for key in db_item[0].__dict__.keys():
        item_data[key] = []
    
    for item in db_item:
        for key, value in zip([item_data[k] for k in item_data.keys()], item.__dict__.values()):
            key.append(value)

    return item_data

