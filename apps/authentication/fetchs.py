from apps.authentication.models import Accomodations, Testimonials, Users, Magazines

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

    magazines = Magazines.query.order_by(Magazines.magazineView.desc()).limit(number).all()

    magazine_data = {}
    
    for key in magazines[0].__dict__.keys():
        magazine_data[key] = []

    for magazine in magazines:
        for key, value in zip([magazine_data[k] for k in magazine_data.keys()], magazine.__dict__.values()):
            key.append(value)
            
    return magazine_data




def fetch_magazines_detail(magazine, number):
    return magazine[number]
