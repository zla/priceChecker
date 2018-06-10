import pprint
import time

from bs4 import BeautifulSoup
import regex
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

pp = pprint.PrettyPrinter(indent=4)


class MainScraper():
    __phantomJSpath = 'C:\\Users\\bogto\\Downloads\\phantomjs-2.1.1-windows'\
                      '\\bin\\phantomjs.exe'

    def __init__(self, scrapeInfo):
        self.name = None
        self.url = None
        self.price = None
        self.code = None
        # if 'code' in scrapeInfo and scrapeInfo['code'] is not None:
        #     self.code = scrapeInfo['code']
        for key in ['name', 'url', 'code']:
            if key in scrapeInfo and scrapeInfo[key] is not None:
                setattr(self, key, scrapeInfo[key])
        if 'link' in scrapeInfo:
            self.url = scrapeInfo['link']

    def show_scraper(self):
        pp.pprint(self.price)

    def _getAsos(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        unavailable = soup.find('div', class_='out-of-stock')
        unavailable = unavailable.find('h3', {'data-bind': 'text:message'})
        if unavailable and regex.search('Out of stock', unavailable.string):
            return None
        elements = soup.find_all('span', {'class': 'current-price'})
        price = elements[0].string
        price = regex.sub(r'[^\d\.,]', '', price)
        browser.quit()
        return price

    def _getEvomag(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        unavailable = soup.find('div', class_='product_right_inside')
        unavailable = unavailable.find('span', class_='stock_stocepuizat')
        if unavailable:
            return None
        element = soup.find('div', class_='pret_rons')
        print(element)
        price = regex.search(r'_rons">([\d,\.]+) <span', str(element))
        try:
            price = price.group(1)
            price = regex.sub(r'\.', '', price)
            price = regex.sub(r',', '.', price)
            browser.quit()
            return price
        except Exception:
            return None

    def _getEmag(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        browser.get(self.url)
        time.sleep(5)
        # browser.find_element_by_xpath(
        #     '//a[contains(@class, "js-load-more")]'
        # ).click()
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        price = None
        # elem = soup.select('div[class*="po-row"]')
        # pp.pprint(elem)
        mainSeller = soup.select('div[class=product-highlight] '
                                 'span[class=text-label] + a')
        if len(mainSeller) == 0:
            mainSeller = 'emag'
        else:
            mainSeller = mainSeller[0]['href']
        mainPrice = soup.find_all('p', class_='product-new-price')
        mainPrice = regex.search(
            r'(?iV1)[\d\.]+<sup>\d{2}', str(mainPrice[0]), regex.M
        ).group()
        if ((self.code == '/emag/1/v' and mainSeller == 'emag') or
                (self.code is not None and self.code == mainSeller)):
            price = mainPrice
        else:
            element = soup.find('a', {'href': self.code})
            if element is None:
                return None
            for prnt in element.parents:
                # try:
                #     temp = prnt['class']
                # except Exception:
                #     continue
                if 'class' not in prnt:
                    continue
                if 'table-md' in prnt['class'] and 'wo-row' in prnt['class']:
                    for child in prnt.descendants:
                        # try:
                        #     temp = child['class']
                        # except Exception:
                        #     continue
                        if 'class' not in child:
                            continue
                        if 'product-new-price' in child['class']:
                            price = regex.search(
                                r'(?iV1)[\d\.]+<sup>\d{2}', str(child), regex.M
                            ).group()
        try:
            price = regex.sub(r'\.|<sup>00', '', price)
            price = regex.sub('<sup>', '.', price)
            price = regex.sub(',', r'\.', price)
        except Exception:
            return None
        browser.quit()
        return price

    def _getAltex(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        element = soup.find('span', {'class': 'Price-int'})
        try:
            price = element.string
        except Exception:
            return None
        price = regex.sub(r'\.', '', price)
        pp.pprint(price)
        browser.quit()
        return price

    def _getAoro(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        pp.pprint(self.code)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        element = soup.find('form', {'name': self.code})
        price = element.find('span', itemprop='price')
        price = price['content']
        pp.pprint(price)
        browser.quit()
        return price

    def _getCel(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        element = soup.find('span', class_='productPrice', itemprop='price')
        try:
            price = element.string
        except Exception:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def _getMobileDirect(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        element = soup.find('meta', itemprop='price')
        try:
            price = element['content']
        except Exception:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def _getQuickmobile(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        element = soup.find('div', class_='product-page-price')
        try:
            price = element['content']
            price = '%.2f' % float(price)
        except Exception:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def _getAmazonDe(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        element = soup.find('span', id='priceblock_ourprice',
                            class_='a-size-medium a-color-price')
        try:
            price = element.string
            price = regex.search(r'([\d,]+)', str(price), regex.M).group()
            price = price.replace(',', '.')
        except Exception:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def _getDualstore(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        element = soup.find('span', id='our_price_display')
        try:
            price = element.string
            price = regex.search(r'([\d,\.]+)', str(price), regex.M).group()
            price = price.replace(',', '')
            price = regex.sub(r'\.00$', '', price)
        except Exception:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def _getPcGarage(self):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(self.url)
        browser.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        # outOfStock = soup.find('p',
        #                        class_='pi-availability outofstock tip hint')
        # pp.pprint(outOfStock)
        # if outOfStock:
        #     return None
        # element = soup.find('p', class_='ps-sell-price')
        # pp.pprint(element)
        pp.pprint(soup)
        price = soup.find('meta', itemprop='price')
        pp.pprint(price)
        # try:
        #     price = soup.find('meta', itemprop='price')
        #     pp.pprint(price)
        #     price = '%.2f' % float(price['content'])
        #     price = element.string
        #     price = regex.search(r'([\d,\.]+)', str(price), regex.M).group()
        #     price = price.replace(',', '')
        #     price = regex.sub(r'\.00$', '', price)
        # except Exception:
        #     return None
        pp.pprint(price)
        browser.quit()
        return price

    def scrape(self):
        if (regex.search(r'asos', self.url)):
            self.price = MainScraper._getAsos(self)
        elif (regex.search(r'evomag', self.url)):
            self.price = MainScraper._getEvomag(self)
        elif (regex.search(r'emag', self.url)):
            self.price = MainScraper._getEmag(self)
        elif (regex.search(r'altex', self.url)):
            self.price = MainScraper._getAltex(self)
        elif (regex.search(r'aoro', self.url)):
            self.price = MainScraper._getAoro(self)
        elif (regex.search(r'cel', self.url)):
            self.price = MainScraper._getCel(self)
        elif (regex.search(r'mobiledirect', self.url)):
            self.price = MainScraper._getMobileDirect(self)
        elif (regex.search(r'quickmobile', self.url)):
            self.price = MainScraper._getQuickmobile(self)
        elif (regex.search(r'amazon\.de', self.url)):
            self.price = MainScraper._getAmazonDe(self)
        elif (regex.search(r'dualstore', self.url)):
            self.price = MainScraper._getDualstore(self)
        elif (regex.search(r'pcgarage', self.url)):
            self.price = MainScraper._getPcGarage(self)


if __name__ == "__main__":
    # product = dict(
    #     name='test',
    #     link='https://www.emag.ro/telefon-mobil-huawei-mate-10-lite-dual-sim'
    #          '-64gb-4g-graphite-black-mate-10-lite-ds-black/pd/D61R30BBM/',
    #     desc='eMAG',
    #     code='/emag/1/v',
    # )
    product = dict(
        name='test',
        link='https://www.pcgarage.ro/smartphone/xiaomi/redmi-5-plus-octa-core'
             '-64gb-4gb-ram-dual-sim-4g-gold/',
    )
    scraper = MainScraper(product)
    # try:
    scraper.scrape()
    scraper.show_scraper()
    # except Exception:
    #     print('Scraping error')
