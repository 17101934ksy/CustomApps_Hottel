import os, hashlib, binascii, re
from urllib.request import urlopen
from bs4 import BeautifulSoup

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
        accomodations_id, accomodations_image, accomodations_name, accomodations_type, accomodations_price = [], [], [], [], []

        for a in btfs.find_all('a', {'class': 'ListItem_container__1z7jK SubhomeList_item__1IR4d'}):
            
            id = re.sub(r'[^0-9]', '', a.get('href'))
            acctype = re.sub(r'[^a-zA-Z]', '', a.get('href'))
            accomodations_type.append(acctype)
            accomodations_id.append(id)

        for div in btfs.find_all('div', {'class': 'ListItem_image__nEbnK'}):

            image_text = div.get('style')
            image = image_text[21:-1] if image_text[:20] == "background-image:url" else ""
            accomodations_image.append(image)

        for div in btfs.find_all('div', {'class': 'ListItem_title__1-j89'}):

            accomodations_name.append(div.text)

        for div in btfs.find_all('div', {'class': 'ListItem_priceContainer__2Asmo'}):
            accomodations_price.append(div.text)

        if len(accomodations_id) == len(accomodations_type) == len(accomodations_image) == len(accomodations_name) == len(accomodations_price):
            for id, acctype, image, name, price in zip(accomodations_id, accomodations_type, accomodations_image, accomodations_name, accomodations_price):
                accomodations_json['Accomodations'].append({"accomodationId": id, "accomodationType": acctype, \
                    "accomodationName": name, "accomodationImage": image, "accomodationPrice": price})
        else: 
            raise IndexError("인덱스 에러")

        return accomodations_json

    def yanolja_rooms():
        return 1
    
    def yanolja_magazine():

        url = urlopen("https://www.yanolja.com/magazine/discover-korea")
        btfs = BeautifulSoup(url, "html.parser")

        magazines_json = {"Accomodations":[]}
        magazines_seq, magazines_id, magazines_thema, magazines_writer, magazines_date, magazines_view, \
            magazines_title, magazines_subtitle, magazines_content, magazines_link, magazines_tag, magazines_image = \
            [], [], [], [], [], [], [], [], [], [], [], []

        for a in btfs.find_all('a', {'class': 'Unit_container__3i4u5'}):
            
            magazine_link = a.get('href')
            magazines_link.append("https://www.yanolja.com" + magazine_link)

        for div in btfs.find_all('div', {'class': 'ImageFallback_body__UgBLm'}):
            
            magazine_style = div.get('style')
            magazine_image = magazine_style[21:-1] if magazine_style[:20] == "background-image:url" else ""
            magazines_image.append(magazine_image)

        for p in btfs.find_all('p', {'class': 'Unit_badge__3bA65'}):
        
            magazine_thema = p.contents[0]
            magazines_thema.append(magazine_thema)

        for link in magazines_link:
            url = urlopen(link)

            for h1 in btfs.find_all('h1', {'class': 'IntroA_title__2e7J_'}):
        
                magazine_title = h1.contents[0]
                magazines_title.append(magazine_title)

            for p in btfs.find_all('p', {'class': 'IntroA_subTitle__3WobL'}):

                magazine_subtitle = p.contents[0]
                magazines_subtitle.append(magazine_subtitle)

            for div in btfs.find_all('div', {'class': 'CaptionA_container__3JeNU'}):

                magazine_writer = div.contents[0].split(" ")[-1]
                magazines_writer.append(magazine_writer)

            for div in btfs.find_all('div', {'class': 'CaptionA_container__3JeNU'}):

                magazine_content = div.contents[0]
                magazines_content.append(magazine_content)

            
        return 1


    action = {
        "Accomodations": yanolja_accomodations(),
        "Rooms": yanolja_rooms(),
        "Magazine": yanolja_magazine()
    }

    return action[dbname]

