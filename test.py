import requests, re
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime, random

def testjson():
    url = urlopen("https://www.yanolja.com/hotel")
    btfs = BeautifulSoup(url, "html.parser")

    accomodations_json = {"Accomodations":[]}
    accomodations_id = []
    accomodations_image = []
    accomodations_name = []
    accomodations_price = []

    for a in btfs.find_all('a', {'class': 'ListItem_container__1z7jK SubhomeList_item__1IR4d'}):

        id = re.sub(r'[^0-9]', '', a.get('href'))
        accomodations_id.append(id)

    for div in btfs.find_all('div', {'class': 'ListItem_image__nEbnK'}):

        image_text = div.get('style')
        image = image_text[21:-1] if image_text[:20] == "background-image:url" else ""
        accomodations_image.append(image)

    for div in btfs.find_all('div', {'class': 'ListItem_title__1-j89'}):

        accomodations_name.append(div.text)

    for div in btfs.find_all('div', {'class': 'ListItem_priceContainer__2Asmo'}):
        accomodations_price.append(div.text)

    if len(accomodations_id) == len(accomodations_image) == len(accomodations_name) == len(accomodations_price):
        for id, image, name, price in zip(accomodations_id, accomodations_image, accomodations_name, accomodations_price):
            accomodations_json['Accomodations'].append({"accomodationId": id, "accomodationName": name, \
                "accomodationImage": image, "accomodationPrice": price})
    else: 
        raise IndexError("인덱스 에러")

    return json.dumps(accomodations_json)


def test_magazine():

    url = urlopen("https://www.yanolja.com/magazine/discover-korea")
    btfs = BeautifulSoup(url, "html.parser")

    magazines_json = {"Accomodations":[]}
    magazines_seq, magazines_id, magazines_thema, magazines_writer, magazines_date, magazines_view, \
        magazines_title, magazines_subtitle, magazines_content, magazines_link, magazines_tag, magazines_image = \
        [], [], [], [], [], [], [], [], [], [], [], []

    for idx, a in enumerate(btfs.find_all('a', {'class': 'Unit_container__3i4u5'})):
        
        magazine_link = a.get('href')
        magazines_link.append("https://www.yanolja.com" + magazine_link)

    for idx, div in enumerate(btfs.find_all('div', {'class': 'ImageFallback_body__UgBLm'})):
        
        magazine_style = div.get('style')
        magazine_image = magazine_style[21:-1] if magazine_style[:20] == "background-image:url" else ""
        magazines_image.append(magazine_image)

    for p in btfs.find_all('p', {'class': 'Unit_title__2o7CO'}):
        
        magazine_title = p.contents[0]
        magazines_title.append(magazine_title)

    for link in magazines_link:
        url = urlopen(link)
        btfs = BeautifulSoup(url, "html.parser")

        for p in btfs.find_all('p', {'class': 'IntroA_subTitle__3WobL'}):

            magazine_subtitle = p.contents[0]
            magazines_subtitle.append(magazine_subtitle)

        for div in btfs.select_one('div.BodyA_container__3Bm2W'):
            magazine_content = div
            magazines_content.append(magazine_content)

    print(len(magazines_subtitle))
    while (len(magazines_link) != len(magazines_subtitle)):
        if len(magazines_link) > len(magazines_subtitle):
            magazines_subtitle.append(magazines_subtitle[-1])
        elif len(magazines_link) < len(magazines_subtitle):
            magazines_subtitle.pop()

    for _ in range(len(magazines_link)):
        magazines_date.append(datetime.datetime.now())
        magazines_view.append(random.randint(1, 1000))


    print(len(magazines_link))
    print(len(magazines_image))
    print(len(magazines_title))
    print(len(magazines_subtitle))
    # print(magazines_writer)
    # print(magazines_content)
    print(len(magazines_content))
    # print(len(magazines_tag))



def test(*args):

    testclass = {
        "test": 0,
        "trr": 0
    }

    testclass['test'] = args[0]
    testclass['trr'] = args[1]

    print(testclass)

class TestData():

    def __init__(self):
        self.a = '10'
        self.b = '12'

if __name__ == "__main__":
    # t = testjson()
    # print(t)
    # print(type(t))

    # test = test_magazine()

    # test = TestData()

    # print(test.__dict__.values())

    test('122', '32')