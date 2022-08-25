from apps.authentication.models import Accomodations

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

def fetch_about(number):
    return number