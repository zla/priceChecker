import pprint
# import sqlite3
from sqlite3 import dbapi2 as sqlite
import time

import numpy as np
import pandas as pd
import regex
# import sqlalchemy as sa
from sqlalchemy import create_engine

import lib.cfg as cfg

pp = pprint.PrettyPrinter(indent=4)


def dbConn():
    e = create_engine('sqlite+pysqlite:///%s' % cfg.db, module=sqlite)
    return e.connect()


def getSessionId():
    conn = dbConn()
    conn.execute(cfg.dels['sessions'])
    result = conn.execute(cfg.queries['nextId'])
    return result.first()['nextId']


def insertSession(dt):
    conn = dbConn()
    conn.execute(cfg.inserts['session'] % (cfg.tables['sessions'], dt))
    return 1


def insertPrice(prod, sesh, price):
    conn = dbConn()
    conn.execute(cfg.inserts['price'] % (cfg.tables['prices'],
                                         prod, sesh, price))
    return 1


def getProducts(what):
    conn = dbConn()
    pDf = pd.read_sql(cfg.queries['%sProds' % what], conn)
    pDf.set_index(keys='product_id', inplace=True)
    return pDf
    # result = conn.execute(cfg.queries['%sProds' % what])
    # products = []
    # for prod in result.fetchall():
    #     p = dict(id=prod[0], name=prod[1], link=prod[2], sheet=prod[3])
    #     if (prod[4]):
    #         p['code'] = prod[4]
    #     products.append(p)
    # return products


def get_db_products():
    conn = dbConn()
    result = conn.execute(cfg.queries['activeProds'])
    products = []
    for prod in result.fetchall():
        p = dict(id=prod[0], name=prod[1], link=prod[2], sheet=prod[3])
        if prod[4]:
            p['code'] = prod[4]
        if prod[5]:
            p['desc'] = prod[5]
        products.append(p)
    return products


def getPrice(pid, sesh):
    conn = dbConn()
    result = conn.execute(cfg.queries['price'] % (cfg.tables['prices'],
                                                  pid, sesh))
    last_price = regex.sub(',', '.', str(result.first()['price']))
    return last_price


def setProdStatus(pid, status):
    if status in ['0', '1']:
        conn = dbConn()
        conn.execute(cfg.updates['prodStatus'] % (cfg.tables['products'],
                                                  status, pid))
        return 1
    else:
        return 'x'


def addProduct(name, url, status, store, sheet):
    conn = dbConn()
    conn.execute(cfg.inserts['prod'] % (cfg.tables['products'], name, url,
                                        status, store, sheet))
    return 1


def activePrices():
    conn = dbConn()
    pDf = pd.read_sql(cfg.queries['activePrices'], conn,
                      parse_dates={'date': '%d-%m-%Y'})
    pDf = pDf.pivot(index='date', columns='product_id', values='price')
    temp = pDf.columns
    date = time.strftime("%Y-%m-%d")
    for col in temp:
        if pDf.loc[date, col] == 'None':
            pDf.drop(labels=[col], axis=1, inplace=True)
    return pDf


def dailyReport(df):
    today = time.strftime("%Y-%m-%d")
    df.replace('None', np.nan, inplace=True)
    priceDiff = df.diff()
    pctDiff = df.pct_change()
    # pp.pprint(pctDiff.tail())
    small = df.min(axis=0)
    big = df.max(axis=0)
    mean = (big + small) / 2
    last = df.loc[today, ]
    lPriceDiff = priceDiff.loc[today, ]
    lPctDiff = pctDiff.loc[today, ]
    report = ''
    prods = getProducts('active')
    # pp.pprint(prods)
    for p in lPctDiff.index:
        if lPctDiff.loc[p] <= -0.05:
            n = prods.loc[p, 'name']
            if prods.loc[p, 'desc'] is not None:
                n += ' %s' % prods.loc[p, 'desc']
            temp = cfg.prodTemplate % (p, n, prods.loc[p, 'url'],
                                       lPctDiff.loc[p] * 100,
                                       lPriceDiff.loc[p], last.loc[p],
                                       big.loc[p], small.loc[p], mean.loc[p])
            report += temp
    return report


def main():
    # test = getProducts('active')
    # test.apply(lambda r: print('%s. %s' % (r.id, r['name'])), axis=1)
    test = dailyReport(activePrices())
    pp.pprint(test)


if __name__ == '__main__':
    main()
