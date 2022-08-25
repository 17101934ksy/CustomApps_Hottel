import requests, re
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

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

if __name__ == "__main__":
    t = testjson()
    print(t)
    print(type(t))