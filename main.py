
import requests
from urllib.parse import urlparse

from annotation import Ozon, Megamarket
import datetime


NAME = "name"
PRICE = "price"
CARD_PRICE = "card_price"
DATE_NOW = "date_now"
IS_ACTUAL = "is_actual"


def main():
    url = (
        '''
https://megamarket.ru/catalog/details/karabin-tundra-krep-din5299s-6h60-mm-ocinkovannyy-100-sht-100066621689/#?related_search=%D0%BA%D0%B0%D1%80%D0%B0%D0%B1%D0%B8%D0%BD%D1%8B
        '''
    )
    print(getDataGivenUrl(url))




def getDataGivenUrl(url):
    url = url.strip()
    if ("ozon" in url.lower()):
        cookies = Ozon().getCookies()
    elif ("megamarket" in url.lower()):
        cookies = Megamarket().getCookies()
    else:
        return "This store is not supported", True

    response = requests.get(url=url, headers=getHeaders(url), cookies=cookies)
    if 200 <= response.status_code < 300:
        if("ozon" in url.lower()):
            ozon = Ozon(response)
            return getNewJsonDataStore(ozon.name, ozon.price, ozon.card_price, ozon.is_actual), True
        elif("megamarket" in url.lower()):
            megamarket = Megamarket(response)
            if (megamarket.name != None or megamarket.price != None):
                return getNewJsonDataStore(megamarket.name, megamarket.price, megamarket.card_price, megamarket.is_actual), True
            else:
                return None, True
        else:
            return None, True

    else:
        return "HTTP response: " + str(response.status_code)


def getNewJsonDataStore(name, price, card_price, is_actual):
    return {
        NAME: name,
        PRICE: price,
        CARD_PRICE: card_price,
        DATE_NOW: str(datetime.datetime.now()),
        IS_ACTUAL: is_actual
    }

def getHeaders(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Origin': base_url,
        'Referer': url
    }

if __name__ == "__main__":
    main()
