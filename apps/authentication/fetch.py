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
    ids, themas, writers, dates, views, titles, subtitles, contents, links, tags, images = [], [], [], [], [], [], [], [], [], [], []

    for magazine in magazines:
        for lists, db_column in zip([ids, themas, writers, dates, views, titles, subtitles, contents, links, tags, images], \
            [magazine.userId, magazine.magazineThema, magazine.magazineWriter, \
                magazine.magazineDate, magazine.magazineView, magazine.magazineTitle, \
                    magazine.magazineSubTitle, magazine.magazineContent, magazine.magazineLink, \
                        magazine.magazineTag, magazine.magazineImage]):
        
            lists.append(db_column)

    return ids, themas, writers, dates, views, titles, subtitles, contents, links, tags, images