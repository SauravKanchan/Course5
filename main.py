from lxml import html
import csv, os, json
import requests
from time import sleep, time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['course']
collection = db['one_plus']


def amazon_parser(url):
    for i in range(10):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        page = requests.get(url, headers=headers)
        doc = html.fromstring(page.content)
        raw_name = doc.xpath('//*[@id="productTitle"]/text()')
        raw_sale_price = doc.xpath('//*[@id="priceblock_dealprice"]/text()')
        raw_category = doc.xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[5]/span/a/text()')
        raw_orignal_price = doc.xpath('//*[@id="newAccordionRow"]/div/div[1]/a/h5/div[2]/div/span[1]/text()[2]')
        raw_availablity = doc.xpath('//*[@id="availability"]/span/text()')
        raw_description = doc.xpath('//*[@id="feature-bullets"]/ul/li[2]/span/text()')
        raw_image = doc.xpath('//*[@id="landingImage"]/@src')
        raw_colour = doc.xpath('//*[@id="variation_color_name"]/div/span/text()')
        raw_star_rating = doc.xpath(
            '//*[@id="prodDetails"]/div[2]/div[2]/div[1]/div[2]/div/div/table/tbody/tr[2]/td[2]/span/span[1]/a[2]/i/span/text()')

        raw_technical_detail = doc.xpath('//*[@id="prodDetails"]/div[2]/div[1]/div[1]/div[2]/div/div/table/tbody/tr/td')
        technical_detail = dict()
        for detail in range(len(raw_technical_detail) // 2):
            technical_detail[raw_technical_detail[detail * 2].text] = raw_technical_detail[detail * 2 + 1].text

        name = ' '.join(''.join(raw_name).split()) if raw_name else None
        sale_price = ' '.join(''.join(raw_sale_price).split()).strip() if raw_sale_price else None
        category = ' > '.join([i.strip() for i in raw_category]) if raw_category else None
        orignal_price = ''.join(raw_orignal_price).strip() if raw_orignal_price else None
        availablity = ''.join(raw_availablity).strip() if raw_availablity else None
        description = ''.join(raw_description).strip() if raw_description else None
        image = ''.join(raw_image).strip() if raw_image else None
        colour = ''.join(raw_colour).strip() if raw_colour else None
        star = ''.join(raw_star_rating).strip() if raw_star_rating else None

        data = {
            'name': name,
            'sale_price': sale_price,
            'category': category,
            'orignal_price': orignal_price,
            'availablity': availablity,
            'description': description,
            'url': url,
            'image': image,
            'colour': colour,
            'technical_detail': technical_detail,
            'star': star,
        }
        if name:
            # print(data)
            break
        else:
            print("Attempts remaining", 9 - i)
            sleep(3)
    return data


def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    AsinList = [
        'B07DJD1Y3Q',
        'B07DJHY82F',
        'B07DJCVTBH',
        'B07DJCJBRD',
        'B07DJHV6VZ',
    ]

    extracted_data = []
    for ind, i in enumerate(AsinList):
        url = "http://www.amazon.in/dp/" + i
        print("Processing: " + url)
        data = amazon_parser(url)
        data["_id"] = int(time() * 10000000)
        extracted_data.append(data)
        sleep(5)
    f = open('data.json', 'w')
    collection.insert_many(extracted_data)
    json.dump(extracted_data, f, indent=4)


if __name__ == "__main__":
    ReadAsin()
