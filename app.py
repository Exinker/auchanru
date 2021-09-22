import os
import json
import time
import random
from datetime import datetime

import requests


URL = 'https://www.auchan.ru/v1/catalog/products'
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
}

def parse_page(page: int):

    # request on the page
    params = {
        'merchantId': 16,
        'page': page,
        'perPage': 40,
        'orderField': 'discountPercent',
        'orderDirection': 'desc',
    }

    response = requests.post(
        url=URL,
        headers=HEADERS,
        params=params,
    )

    # scrape data
    data = []
    for item in response.json()['items']:
        try:
            data.append({
                'title': item['title'],
                'article': item['gimaId'],
                'price': item['price']['value'],
                'discount': item['discount']['size'],
                'category_codes': [el['id'] for el in item['categoryCodes']],
            })

        except Exception as error:
            text = f'error: {error}\npage={page}\nitem={item}\n'
            print(text)

            return []

    return data


def parse_pages(filedir: str):

    data = []

    page = 1
    while True:
        data = parse_page(page)

        if data:
            print(f'page {page} is parsed')

            # save data to file
            filepath = os.path.join(filedir, 'data.json')

            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as file:
                    data.extend(json.load(file))

            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            # go to the next page
            page += 1

            # sleep few moments
            time.sleep(random.random())

        else:
            break


if __name__ == '__main__':

    # create folder to storage
    date = datetime.today().strftime('%Y-%m-%d')

    filedir = os.path.join('.', 'data', date)
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    # parse pages
    parse_pages(filedir)

    # check results
    filepath = os.path.join(filedir, 'data.json')
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
