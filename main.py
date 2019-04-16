from lxml import html
import csv, os, json
import requests
from time import sleep


def amazon_parser(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url, headers=headers)
    doc = html.fromstring(page.content)
    for i in range(10):
        RAW_NAME = doc.xpath('//*[@id="productTitle"]/text()')
        RAW_SALE_PRICE = doc.xpath('//*[@id="priceblock_dealprice"]/text()')
        RAW_CATEGORY = doc.xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[5]/span/a/text()')
        RAW_ORIGINAL_PRICE = doc.xpath('//*[@id="price"]/table/tbody/tr[1]/td[2]/span[1]/text()')
        RAw_AVAILABILITY = doc.xpath('//*[@id="availability"]/span/text()')
        RAw_DESCRIPTION = doc.xpath('//*[@id="feature-bullets"]/ul/li[2]/span/text()')

        NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
        SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
        CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
        ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
        AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
        DESCRIPTION = ''.join(RAw_DESCRIPTION).strip() if RAw_AVAILABILITY else None

        data = {
            'NAME': NAME,
            'SALE_PRICE': SALE_PRICE,
            'CATEGORY': CATEGORY,
            'ORIGINAL_PRICE': ORIGINAL_PRICE,
            'AVAILABILITY': AVAILABILITY,
            'DESCRIPTION': DESCRIPTION,
            'URL': url,
        }
        if NAME:
            print(data)
            break
        else:
            print("Attempt remaining",9-i)
            sleep(2)


def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    AsinList = ['B07DJD1Y3Q',
                # 'B07DJHY82F',
                # 'B07DJCVTBH',
                # 'B07DJCJBRD',
                # 'B07DJHV6VZ',
                ]

    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.in/dp/" + i
        print("Processing: " + url)
        extracted_data.append(amazon_parser(url))
        sleep(5)
    f = open('data.json', 'w')
    json.dump(extracted_data, f, indent=4)


if __name__ == "__main__":
    ReadAsin()
