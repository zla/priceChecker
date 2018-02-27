import pprint
import sqlite3
from sqlite3 import dbapi2 as sqlite
import time

import regex
import sqlalchemy
from sqlalchemy import create_engine

import lib.cfg as cfg
from lib.main_scraper import MainScraper
from lib.sheets_operations import start_service

pp = pprint.PrettyPrinter(indent=4)


def get_session_id():
    e = create_engine('sqlite+pysqlite:///%s' % cfg.db, module=sqlite)
    conn = e.connect()
    conn.execute(cfg.dels['sessions'])
    result = conn.execute(cfg.queries['nextId'])
    return result.first()['nextId']


def insert_session(dt):
    e = create_engine('sqlite+pysqlite:///%s' % cfg.db, module=sqlite)
    conn = e.connect()
    conn.execute(cfg.inserts['session'] % (cfg.tables['sessions'], dt))


def insert_price(prod, session, price):
    e = create_engine('sqlite+pysqlite:///%s' % cfg.db, module=sqlite)
    conn = e.connect()
    conn.execute(cfg.inserts['price'] % (cfg.tables['prices'], prod,
                                         session, price))


def write_price(sheet, date, price):
    service = start_service()
    values = [date, price]
    body = {'values': [values]}
    service.spreadsheets().values().append(spreadsheetId=sheet, range='A3',
                                           valueInputOption='USER_ENTERED',
                                           body=body
                                          ).execute()


def get_db_products():
    e = create_engine('sqlite+pysqlite:///%s' % cfg.db, module=sqlite)
    conn = e.connect()
    result = conn.execute(cfg.queries['activeProds'])
    products = []
    for prod in result.fetchall():
        p = dict(id=prod[0], name=prod[1], link=prod[2], sheet=prod[3])
        if (prod[4]):
            p['code'] = prod[4]
        if (prod[5]):
            p['desc'] = prod[5]
        products.append(p)
    return products


def get_last_price(pid, session):
    e = create_engine('sqlite+pysqlite:///%s' % cfg.db, module=sqlite)
    conn = e.connect()
    result = conn.execute(
        cfg.queries['price'] % (cfg.tables['prices'], pid, session))
    last_price = regex.sub(',', '.', str(result.first()['price']))
    return last_price


def check_new(db, sh):
    new = []
    for psh in sh:
        flag = 0
        for pdb in db:
            if (flag == 1):
                break
            if (psh['link'] == pdb['link']):
                flag = 1
        if (flag == 0):
            new.append(psh)
    return new


if __name__ == '__main__':
    currentId = get_session_id()
    date = '%s 00:00' % time.strftime("%Y-%m-%d")
    dateSh = time.strftime("_%d_%m_%Y")
    productsDb = get_db_products()
    # body = ''
    for prod in productsDb:
        pp.pprint(prod)
        scraper = MainScraper(prod)
        try:
            scraper.scrape()
            scraper.show_scraper()
        except:
            print('Scraping error')
            continue
        prod['price'] = scraper.price
        print(prod['price'])
        if prod['price'] is not None:
            prod['price'] = str(prod['price'])
            # test = float(prod['price']) - float(last_price)
            # if (test <= 0) and (last_price != 'None'):
            #     body += 'Lower price on ' + prod['name'] + ': ' + str(test) + '\n'\
            #         + prod['link'] + '\n\n'
            insert_price(str(prod['id']), str(currentId), str(prod['price']))
            write_price(prod['sheet'], dateSh, prod['price'])
    insert_session(date)
    # pp.pprint(body)
