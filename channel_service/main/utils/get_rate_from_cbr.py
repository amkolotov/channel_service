import requests

import xmltodict


def get_rate_from_cbr(name, date=''):
    """Функция получения курса валюты на указанную дату"""
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    if date:
        url = f'{url}?date_req={date}'
    response = requests.get(url)
    dict_data = xmltodict.parse(response.content)
    rate_dict = list(filter(lambda item: item['Name'] == name, dict_data['ValCurs']['Valute']))[0]
    return rate_dict['Value']
