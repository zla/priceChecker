import pandas as pd
import pprint

import lib.db as db
import lib.cfg as cfg

pp = pprint.PrettyPrinter(indent=4)


def displayMenu():
    print('\tAdmin Menu')
    print('1. View active products')
    print('2. View inactive products')
    print('3. View all products')
    print('4. View full product info')
    print('5. View all product prices')
    print('6. Change product status')
    print('7. View stores')
    print('8. Add product')
    print('x. Exit')


def processOpt(opt):
    if opt == 'x':
        return 'x'
    elif opt in ['1', '2', '3']:
        prods = db.getProducts(cfg.options[opt])
        print('\tProducts:')
        prods.apply(lambda r: print('%s. %s' % (r.id, r['name'])), axis=1)
    elif opt == '4':
        prods = db.getProducts('all')
        pid = 'init'
        while pid != 'x':
            pid = input('Enter the product ID (x to exit): ')
            try:
                temp = prods[prods['id'] == int(pid)]
                temp.apply(
                        lambda r: print(
                                '\n%s. %s\nSheet: %s\n' % 
                                (r.id, r['name'], r.sheet)), 
                        axis=1)
            except:
                pass
    elif opt == '6':
        pid = input('Enter the product ID: ')
        status = input('Enter the new product status (1/0): ')
        db.setProdStatus(pid, status)
    elif opt == '8':
        name = input('Enter the product name: ')
        url = input('Enter the product url: ')
        status = input('Enter the product status (0/1): ')
        store = input('Enter the store id: ')
        sheet = input('Enter the Google Drive sheet id: ')
        db.addProduct(name, url, status, store, sheet)
    input('---')
    return opt


def main():
    opt = 'init'
    while opt != 'x':
        displayMenu()
        opt = input('Enter your choice: ')
        opt = processOpt(opt)


if __name__ == '__main__': main()
