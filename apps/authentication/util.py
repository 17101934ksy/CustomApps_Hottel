import os, hashlib, binascii, requests, re, json
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/


def hash_pass(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""

    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password



def crawler_db(dbname):
    # action_db에 따라 크롤링 데이터 다르게 적용

    def yanolja_accomodations():
        # hot100

        url = urlopen("https://www.yanolja.com/hotel")
        btfs = BeautifulSoup(url, "html.parser")

        accomodations_json = {"Accomodations":[]}
        accomodations_id = []
        accomodations_image = []
        accomodations_name = []
        accomodations_type = []

        for a in btfs.find_all('a', {'class': 'ListItem_container__1z7jK SubhomeList_item__1IR4d'}):
            id = re.sub(r'[^0-9]', '', a.get('href'))
            acctype = re.sub(r'^[a-zA-Z]', '', a.get('href'))
            accomodations_type.append(acctype)
            accomodations_id.append(id)

        for div in btfs.find_all('div', {'class': 'ListItem_image__nEbnK'}):
            image_text = div.get('style')
            image = image_text[21:-1] if image_text[:20] == "background-image:url" else ""
            accomodations_image.append(image)

        for div in btfs.find_all('div', {'class': 'ListItem_title__1-j89'}):
            accomodations_name.append(div.text)

        if len(accomodations_id) == len(accomodations_type) == len(accomodations_image) == len(accomodations_name):
            for id, acctype, image, name in zip(accomodations_id, accomodations_type, accomodations_image, accomodations_name):
                accomodations_json['Accomodations'].append({"accomodationId": id, "accomodationType": acctype, \
                    "accomodationName": name, "accomodationImage": image})
        else: 
            raise IndexError("인덱스 에러")

        return accomodations_json

    def yanolja_rooms():
        return 1
    
    action = {
        "Accomodations": yanolja_accomodations(),
        "Rooms": yanolja_rooms()
    }

    func = action[dbname]

    return func
    