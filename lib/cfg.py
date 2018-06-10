db = 'priceCheckerDb.db'
tables = dict(
    products='product',
    extra='product_extra',
    prices='price',
    archive='archive',
    sessions='session',
)

options = {
    '1': 'active',
    '2': 'inactive',
    '3': 'all',
}

dels = dict(
    sessions='''DELETE FROM %s
        WHERE session_id NOT IN (SELECT session_id FROM %s)''' % (
            tables['prices'], tables['sessions']),
)

inserts = dict(
    session="INSERT INTO %s (date) VALUES ('%s')",
    price='INSERT INTO %s (product_id, session_id, amount) VALUES (%s, %s, %s)',
    prod='''INSERT INTO %s (name, url, active, store_id, sheet)
        VALUES ('%s', '%s', %s, %s, '%s')''',
)

updates = dict(
    prodStatus='UPDATE %s SET active = %s WHERE product_id = %s',
)

queries = dict(
    nextId='SELECT MAX(session_id) + 1 nextId FROM %s' % tables['sessions'],
    activeProds="""SELECT p.product_id, p.name, p.url, p.sheet, e.code, e.desc
        FROM %s p
        LEFT JOIN %s e ON p.product_id = e.product_id
        WHERE p.active = 1""" % (tables['products'], tables['extra']),
    inactiveProds="""SELECT p.product_id, p.name, p.url, p.sheet, e.code, e.desc
        FROM %s p
        LEFT JOIN %s e ON p.product_id = e.product_id
        WHERE p.active = 0""" % (tables['products'], tables['extra']),
    allProds="""SELECT p.product_id, p.name, p.url, p.sheet, e.code, e.desc
        FROM %s p
        LEFT JOIN %s e ON p.product_id = e.product_id""" % (tables['products'],
                                                            tables['extra']),
    price="""SELECT amount
        FROM %s
        WHERE product_id = %s AND session_id = %s""",
    activePrices="""SELECT p.product_id, se.date, e.amount
        FROM %s e
        JOIN %s se ON e.session_id = se.id
        JOIN %s p ON e.product_id = p.product_id
        WHERE p.active = 1 AND e.amount IS NOT NULL""" % (
            tables['prices'], tables['sessions'], tables['products']),
)

prodTemplate = '\n%d. %s\n%s\n%.3f%% (%.2f RON) from yesterday\nTODAY: %.2f, '\
               'HI: %.2f, LOW: %2.f, MEAN: %2.f\n'
