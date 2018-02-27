from __future__ import print_function
import httplib2
import os
import pprint
import time

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

from lib.main_scraper import MainScraper
from lib.settings import bogdanSpreadsheetId as spreadsheetId

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'
pp = pprint.PrettyPrinter(indent=4)


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    cred_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(cred_dir):
        os.makedirs(cred_dir)
    cred_path = os.path.join(cred_dir,
                             'sheets.googleapis.com-python-quickstart.json')

    store = Storage(cred_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + cred_path)
    return credentials


def start_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service


def row_range_to_list(range):
    list = []
    for row in range:
        for i in row:
            list.append(i)
    return list


def col_range_to_list(range):
    list = []
    for col in range:
        for i in col:
            list.append(i)
    return list


def get_named_range(service, spreadsheet, range):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet,
                                                 range=range).execute()
    return result.get('values', [])


def get_col_range(service, spreadsheet, range):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet,
                                                 range=range).execute()
    return result.get('values', [])


def display_range(rng):
    if not rng:
        print('No data found.')
    else:
        pp.pprint(rng)


def get_sh_products(service, spreadsheetId):
    names = get_named_range(service, spreadsheetId, 'products')
    names = row_range_to_list(names)
    links = get_named_range(service, spreadsheetId, 'links')
    links = row_range_to_list(links)
    products = []
    for n, l in zip(names, links):
        product = dict(name=n, link=l)
        products.append(product)
    return products


def main():
    service = start_service()
    products = get_sh_products(service, spreadsheetId)
    columns = len(products) + 1
    date = time.strftime("_%d_%m_%Y")
    row_num = get_col_range(service, spreadsheetId, 'A3:A')
    row_num = col_range_to_list(row_num)
    row_num = len(row_num) + 3
    values = [date]
    for prod in products:
        pp.pprint(prod)
        scraper = MainScraper(prod)
        scraper.scrape()
        scraper.show_scraper()
        prod['price'] = str(scraper.price)
        print(prod['price'])
        values = values + [prod['price']]
    body = {'values': [values]}
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range='A3',
        valueInputOption='USER_ENTERED', body=body).execute()
    requests = []
    # requests.append(dict(findReplace=dict(find=date, matchEntireCell=True,
    #                                       sheetId=0)))
    requests.append(
        dict(
            addNamedRange=dict(
                namedRange=dict(
                    name="{date}".format(**vars()),
                    range=dict(
                        sheetId=0,
                        startColumnIndex=0,
                        endColumnIndex=columns,
                        startRowIndex=row_num - 1,
                        endRowIndex=row_num
                    )
                )
            )
        ))
    body = dict(requests=requests)
    response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId,
                                                  body=body).execute()
    find_response = response.get('replies')
    pp.pprint(find_response)


if __name__ == '__main__':
    main()
