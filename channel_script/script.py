import os
import time
from datetime import datetime
from decimal import Decimal

import gspread
import psycopg2
import requests
import xmltodict


GOOGLE_SHEETS_CREDENTIALS = {
    "type": "service_account",
    "project_id": "channel-service-350903",
    "private_key_id": "11a89af9af290bf4875e909f193a80ee03fadade",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCym4RrjjGtmXfp\n05fJf6/6zzZP/3FzXPJLHdFxFBvR7+T4p7TOZHcbsGey/Hw8oW7tocvL68PGWz5F\niNVOvIznNIHW6Ovq5bLzRdrUx8tw8Xx6ar9v2WiJYMHrYvL2Mxe+0rj+b/MibBOz\nQaG69YB3MunR56xuJnNqgYZYqQHCzmp9xsRI4be86FiJ6sjh4WUZXrkuiP08kaU2\nuceUIdOmWK8+BUcE1SwCgBX/rj163HouOvmsPAH2sFvG6KBHxU13y0CT2IVwjR5E\nDQbwoV4ipUKPrkccp7HrE9k/pSCMd2L7NrRoOd4VMZ1PsB4recYYXkrM54UlccQa\n0ANGoYlpAgMBAAECgf9QDuWMUHB0IBZf+ThQWavIAJmXwihYTZFNmlAHH7xYne9E\nhefFm8LH5oqU8BfAFZxjZ+KxxTw77So8gNkcMef2utJ4Qm99GvjbkrRELEpElfn1\n5WNp/0mcSoKhv/in4r8CCfJiGkwhYdByyTh1VRYAWBH2xKHFvfZ+BxDxLNBdQOcG\npTGpymj+ULWG9dDRwj0tCLClGP07LjSrkv8Uk8l8iEH+6wf2SwjS4xudbSvfEDaz\nhZvSEjPQwxl6coXFERTQQLfB7K2cQyz0dFf7Geyv30x1P5CggDIvgb7WtlwQLZdN\nlsCnWfY8Ic8wbRSKjOzemtB5UxpYS8UfLJr8yyECgYEA+UV5OtIsNN7UHr7TwnLG\n3H9RCKImKqCCvUKtrdR3JbbswwRBpoSaFwAzuwgoaWAduXeSgRZKksbIEJ8xMsTU\n+nH86erPXRu3R4UWND/B6rrW1MaXXRxSpXO4FpPbm+ocnd6Cnrsc13nM2BBL+IqC\nB4kCVP9qHekScqRYyKpK5NkCgYEAt229Jp06FpdNOHi5rSFpmgmMmCqy1laFSVUG\ntZHEoYXa7LiJAUGZWMqzIYP+xpy7N3p0d9JVxnJbYF7T3s4Io5qIjUuTnn49f0Ev\nC7lcmCFtakKSH0Or5HOPOdAiUCZ0FOj9lNssYnDL2khY8vKpvIHoGVJ6cXRfD9Vn\nqcv4rxECgYBgg6zHwJ7LLcfVy680J7qln0oh3J6IfLOCUjHrD0u+t4/+hkRhFBCR\nfUuKTENRYZzAtfJsttPS9tJ51Rl4fcu02LPDYl49v8B8GaSaQGF14DfUFLyAmbnK\nQ/7wBvnN6ZyA56mNigdFyuwscErqBb8I6dyUSnys7hRtfQK/V2g+KQKBgEsw9/XJ\nQ9OY6DW6/1oiNTjIq1KBRlgolXCvIxXxECqqRUj+iGL0chj81ptpkVn3S6N9Vhr8\nJN85Z43EsZNG4DG4mjtZfMTeuPTeUpu6u2M9aK3DZkTcp6z5Vf/7+uTiLnmX3MNV\naQddd6MePyAwKzY0BmHC9qBldMZ304u+Kk4RAoGBANUYuLaWy11jdUoN4vZUcWHP\nscUmKOD1TIAq0ppc/dtoUQ1NvIvMBYysCXwM/HOLyzj6ozk7YW4LBWugVEYcyFYK\nkbtTWGvZLXiYoEjNeh51imZXYxJPX21PboI2n5Je6rJuD6ySudNDu/WiN1RlYC4K\nWIZmb4n/2eO8hVWd6kgL\n-----END PRIVATE KEY-----\n",
    "client_email": "channel-service@channel-service-350903.iam.gserviceaccount.com",
    "client_id": "100713502371838679897",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/channel-service%40channel-service-350903.iam.gserviceaccount.com"
}
SPREAD_SHEET_NAME = 'Заявки Канал Сервис'
SHEET_NAME = 'Заявки'
scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]


def get_values_from_gs():
    """Функция получения данных из google sheets"""
    try:
        client = gspread.service_account_from_dict(GOOGLE_SHEETS_CREDENTIALS, scope)
        spread = client.open(SPREAD_SHEET_NAME)
        worksheet = spread.worksheet(SHEET_NAME)
        list_of_lists = worksheet.get_all_values()
        return list_of_lists
    except Exception as e:
        print(f'Get values from Google Sheets error: {e}')


def get_rate_usd_from_cbr():
    """Функция получения курса доллара США"""
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    try:
        response = requests.get(url)
        dict_data = xmltodict.parse(response.content)
        rate = tuple(filter(lambda item: item['Name'] == 'Доллар США', dict_data['ValCurs']['Valute']))[0]['Value']
        return rate
    except Exception as e:
        print(f'Get usd rate from cbr error: {e}')
        return


def send_message_to_telegram(chat_id, message):
    """Функция отправления сообщения в телеграмм"""
    bot_token = '5320735825:AAF5g6KKBRU2iG8I3a4ioVh8fKTMKrjk8UE'

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
    response = requests.get(url)
    return response.json()


def get_formatted_bid(bid_tuple):
    """Функция форматирования представления заявки"""
    return ', '.join((str(bid_tuple[0]), str(bid_tuple[1]), str(round(float(bid_tuple[2]), 2)), datetime.strftime(bid_tuple[4], '%d.%m.%Y')))


def save_values_in_db(values_list, usd_rate):
    """Функция сохранения данных в БД"""
    conn = psycopg2.connect(database='channel_db', user='channel', password='channel',
                            host=os.environ.get('HOST_DB', 'localhost'), port='5432')
    cursor = conn.cursor()
    # cursor.execute('''DROP TABLE bid;''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bid (id serial NOT NULL PRIMARY KEY, number integer NOT NULL, bid_id integer NOT NULL, price_usd decimal NOT NULL, price_rub decimal NOT NULL, delivery_time date NOT NULL, created_at timestamp NOT NULL);''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS "bid_bid_id_idx" ON bid (bid_id);''')
    conn.commit()

    cursor.execute('''SELECT bid_id FROM bid ORDER BY number ASC''')
    bid_ids = [ids[0] for ids in cursor.fetchall()]

    insert_query = '''INSERT INTO bid (number, bid_id, price_usd, price_rub, delivery_time, created_at) VALUES (%s, %s, %s, %s, %s, %s)'''
    update_query = '''UPDATE bid SET price_usd = %s, price_rub = %s, delivery_time = %s WHERE bid_id = %s'''
    get_query = '''SELECT number, bid_id, price_usd, price_rub, delivery_time, created_at FROM bid WHERE bid_id = %s'''
    delete_query = '''DELETE FROM bid WHERE bid_id = %s'''

    added_list = []
    changed_list = []
    remove_list = []

    for row in values_list:
        if row[1]:
            try:
                cursor.execute(get_query, (int(row[1]),))
                bid_db = cursor.fetchone()
                item_tuple = (int(row[0]), int(row[1]), Decimal(row[2]), Decimal(row[2]) * Decimal(usd_rate.replace(',', '.')),
                             datetime.strptime(row[-1], '%d.%m.%Y').date(), datetime.now())
                if (item_tuple[4] < datetime.now().date()):
                    message = f'Вышел срок реализации заявки:\n{get_formatted_bid(item_tuple)}'
                    if os.environ.get('CHAT_ID', ''):
                        send_message_to_telegram(os.environ.get('CHAT_ID', ''), message)
                if not bid_db:
                    cursor.execute(insert_query, item_tuple)
                    conn.commit()
                    added_list.append(item_tuple)
                else:
                    indexes = (0, 1, 2, 4)
                    for i in indexes:
                        if bid_db[i] != item_tuple[i]:
                            cursor.execute(update_query, (item_tuple[2], item_tuple[3], item_tuple[4], item_tuple[1]))
                            conn.commit()
                            changed_list.append(item_tuple)
                    bid_ids.remove(item_tuple[1])
            except Exception as e:
                print(f'Save db error: {e}')
    if bid_ids:
        for bid_id in bid_ids:
            cursor.execute(get_query, (bid_id,))
            del_bid = cursor.fetchone()
            remove_list.append(del_bid)
            cursor.execute(delete_query, (bid_id,))
            conn.commit()

    if added_list:
        print('Добавленные заявки:')
        for added_bid in added_list:
            print(get_formatted_bid(added_bid))
    else:
        print('Нет добавленных заявок')

    if changed_list:
        print('Измененные заявки:')
        for changed_bid in changed_list:
            print(get_formatted_bid(changed_bid))
    else:
        print('Нет измененных заявок')

    if remove_list:
        print('Удаленные заявки:')
        for removed_bid in remove_list:
            print(get_formatted_bid(removed_bid))
    else:
        print('Нет удаленых заявок')

    if conn:
        cursor.close()
        conn.close()


def start():
    while True:
        values = get_values_from_gs()
        rate = get_rate_usd_from_cbr()
        if values and rate:
            save_values_in_db(values[1:], rate)
        time.sleep(60)


if __name__ == '__main__':
    start()
