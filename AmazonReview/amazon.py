from lxml import html
import csv, os, json
import requests
from exceptions import ValueError
from time import sleep


def AmzonParser(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url, headers=headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
            XPATH_RATINGS = '//div[contains(@id, "rev-dpReviewsMostHelpfulAUI")]/div/div/a/i/span//text()'
            XPATH_REVIEWS_TITLE = '//div[contains(@id, "rev-dpReviewsMostHelpfulAUI")]/div/div/a[2]//text()'
            XPATH_REVIEWS_BODY = '//div[contains(@id, "revData-dpReviewsMostHelpfulAUI")]/div//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            RAW_RATINGS = doc.xpath(XPATH_RATINGS)
            RAW_REVIEWS_TITLE = doc.xpath(XPATH_REVIEWS_TITLE)
            RAW_REVIEWS_BODY = doc.xpath(XPATH_REVIEWS_BODY)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
            RATINGS = ' , '.join(RAW_RATINGS).strip() if RAW_RATINGS else None
            REVIEWS_TITLE = ' , '.join(RAW_REVIEWS_TITLE).strip() if RAW_REVIEWS_TITLE else None
            REVIEWS_BODY = ' , '.join(RAW_REVIEWS_BODY).strip() if RAW_REVIEWS_BODY else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code != 200:
                raise ValueError('captha')

            # RATINGS = RATINGS.replace(" out of 5 stars", "")
            data = {
                'NAME': NAME,
                'SALE_PRICE': SALE_PRICE,
                'CATEGORY': CATEGORY,
                'ORIGINAL_PRICE': ORIGINAL_PRICE,
                'AVAILABILITY': AVAILABILITY,
                'URL': url,
                'RATINGS': RATINGS,
                'REVIEWS_TITLE': REVIEWS_TITLE,
                'REVIEWS_BODY': REVIEWS_BODY,
            }

            return data
        except Exception as e:
            print e


def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    AsinList = ['B0046UR4F4',
                'B00JGTVU5A',
                'B00GJYCIVK',
                'B00EPGK7CQ',
                'B00EPGKA4G',
                'B00YW5DLB4',
                'B00KGD0628',
                'B00O9A48N2',
                'B00O9A4MEW',
                'B00UZKG8QU',
                ]
    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.com/dp/" + i
        print "Processing: " + url
        extracted_data.append(AmzonParser(url))
        sleep(5)
    f = open('data.json', 'w')
    json.dump(extracted_data, f, indent=4)


if __name__ == "__main__":
    ReadAsin()
