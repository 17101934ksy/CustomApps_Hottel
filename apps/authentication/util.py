import os, hashlib, binascii, re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime, random

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

        magazines_json = {"Magazines":[]}
        magazines_thema, magazines_writer, magazines_date, magazines_view, \
            magazines_title, magazines_subtitle, magazines_content, magazines_link, magazines_tag, magazines_image = \
                [], [], [], [], [], [], [], [], [], []

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

            if magazine_thema == '여행':
                magazines_tag.append('#여행 #여행스타그램 #떠나고싶다 #여행에미치다 #일상을여행처럼 #여행사진 #여행후기 #여행중 #여행기록 #여행일기 #여행중독 #여행앓이 #추억스타그램 #추억 #비행스타그램 #떠나자 #떠나자그램 #놀러가자 #휴가스타그램 #소통 #행복 #선팔 #맞팔 #팔로우 #좋아요')
            elif magazine_thema == '미식':
                magazines_tag.append('#미식 #먹방 #먹스타그램 #먹스타 #맛스타 #맛스타그램 #맛있다 #푸드스타그램 #또먹고싶다 #맛집 #먹방투어 #맛집투어 #카페투어 #카페스타그램 #디저트그램 #오늘뭐먹지 #좋아요 #소통 #선팔 #맞팔 #팔로우 #foodfic #instagood')
            elif magazine_thema == '숙소':
                magazines_tag.append('#숙소 #숙소스타그램 #호캉스 #호텔 #모텔 #풀빌라 #숙스타그램 #휴식은 숙소지')
            else:
                magazines_tag.append(f'#{magazine_thema}')

        for p in btfs.find_all('p', {'class': 'Unit_title__2o7CO'}):
            magazine_title = p.contents[0]
            magazines_title.append(magazine_title)

        for writer in range(len(magazines_link)):
            magazines_writer.append("writer_" + str(writer))

        for link in magazines_link:
            url = urlopen(link)
            btfs = BeautifulSoup(url, "html.parser")

            for p in btfs.find_all('p', {'class': 'IntroA_subTitle__3WobL'}):
                magazine_subtitle = p.contents[0]
                magazines_subtitle.append(magazine_subtitle)
   
            for div in btfs.select_one('div.BodyA_container__3Bm2W'):
                magazine_content = div
                magazines_content.append(magazine_content)

        for _ in range(len(magazines_link)):
            magazines_date.append(datetime.datetime.now())
            magazines_view.append(random.randint(1, 1000))

        while (len(magazines_link) != len(magazines_subtitle)):
            if len(magazines_link) > len(magazines_subtitle):
                magazines_subtitle.append(magazines_subtitle[-1])
            elif len(magazines_link) < len(magazines_subtitle):
                magazines_subtitle.pop()

        if len(magazines_thema) == len(magazines_writer) == len(magazines_date) == len(magazines_view) == len(magazines_title) == \
            len(magazines_subtitle) == len(magazines_content) == len(magazines_link) == len(magazines_tag) == len(magazines_image):
            
            for thema, writer, date, view, title, subtitle, content, link, tag, image in zip(magazines_thema, magazines_writer, magazines_date, magazines_view, magazines_title, \
                magazines_subtitle, magazines_content, magazines_link, magazines_tag, magazines_image):
                magazines_json['Magazines'].append({"magazineThema": thema, "magazineWriter": writer, \
                    "magazineDate": date, "magazineView": view, "magazineTitle": title, \
                        "magazineSubTitle": subtitle, "magazineContent": content, "magazineLink": link, \
                            "magazineTag": tag, "magazineImage": image})
        else: 
            raise IndexError("인덱스 에러")

        return magazines_json


    action = {
        "Accomodations": yanolja_accomodations(),
        "Rooms": yanolja_rooms(),
        "Magazines": yanolja_magazine()
    }

    return action[dbname]

