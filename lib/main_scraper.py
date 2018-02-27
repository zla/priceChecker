import pprint
import time

from bs4 import BeautifulSoup
import regex
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

pp = pprint.PrettyPrinter(indent=4)


class MainScraper():
    __phantomJSpath = 'C:\\Users\\bogto\\Downloads\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'

    def __init__(self, scrapeInfo):
        self.name = scrapeInfo['name']
        self.url = scrapeInfo['link']
        self.price = None
        self.code = None
        if ('code' in scrapeInfo and scrapeInfo['code'] is not None):
            self.code = scrapeInfo['code']

    def show_scraper(self):
        pp.pprint(self.price)

    def __getAsos(url):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        unavailable = soup.find('div', class_='out-of-stock')
        unavailable = unavailable.find('h3', {'data-bind': 'text:message'})
        if unavailable and regex.search('Out of stock', unavailable.string):
            return None
        elements = soup.find_all('span', {'class': 'current-price'})
        price = elements[0].string
        price = regex.sub(r'[^\d\.,]', '', price)
        browser.quit()
        return price

    def __getEvomag(url):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(url)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
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
        except:
            return None

    def __getEmag(url, code):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(url)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        price = None
        mainSeller = soup.select(
            "div[class=product-highlight] span[class=text-label] + a")
        if len(mainSeller) == 0:
            mainSeller = 'emag'
        else:
            mainSeller = mainSeller[0]['href']
        mainPrice = soup.find_all('p', class_='product-new-price')
        mainPrice = regex.search(r"(?iV1)[\d\.]+<sup>\d{2}", str(mainPrice[0]),
                                 regex.M).group()
        if ((code is None and mainSeller == 'emag') 
                or (code is not None and code == mainSeller)):
            price = mainPrice
        else:
            element = soup.find('a', {'href': code})
            if element is None:
                return None
            for prnt in element.parents:
                try:
                    temp = prnt['class']
                except:
                    continue
                if ('table-md' in prnt['class'] and 'wo-row' in prnt['class']):
                    for child in prnt.descendants:
                        try:
                            temp = child['class']
                        except:
                            continue
                        if 'product-new-price' in child['class']:
                            price = regex.search(r"(?iV1)[\d\.]+<sup>\d{2}",
                                                 str(child), regex.M).group()
        try:
            price = regex.sub(r'\.|<sup>00', '', price)
            price = regex.sub('<sup>', '.', price)
            price = regex.sub(',', r'\.', price)
        except:
            return None
        browser.quit()
        return price

    def __getAltex(url):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(url)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        element = soup.find('span', {'class': 'Price-int'})
        try:
            price = element.string
        except:
            return None
        price = regex.sub(r'\.', '', price)
        pp.pprint(price)
        browser.quit()
        return price

    def __getAoro(url, code):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(url)
        pp.pprint(code)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        element = soup.find('form', {'name': code})
        price = element.find('span', itemprop='price')
        price = price['content']
        pp.pprint(price)
        browser.quit()
        return price

    def __getCel(url):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(url)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        element = soup.find('span', class_='productPrice', itemprop='price')
        try:
            price = element.string
        except:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def __getMobileDirect(url):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(url)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        element = soup.find('meta', itemprop='price')
        try:
            price = element['content']
        except:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def __getQuickmobile(url):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(url)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        element = soup.find('div', class_='product-page-price')
        try:
            price = element['content']
            price = '%.2f' % float(price)
        except:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def __getAmazonDe(url):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(url)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        element = soup.find(
                'span', id='priceblock_ourprice', 
                class_='a-size-medium a-color-price')
        try:
            price = element.string
            price = regex.search(r"([\d,]+)", str(price), regex.M).group()
            price = price.replace(',', '.')
        except:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def __getDualstore(url):
        browser = webdriver.PhantomJS(MainScraper.__phantomJSpath)
        print(url)
        browser.get(url)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        element = soup.find('span', id='our_price_display')
        try:
            price = element.string
            price = regex.search(r"([\d,\.]+)", str(price), regex.M).group()
            price = price.replace(',', '')
            price = regex.sub(r'\.00$', '', price)
        except:
            return None
        pp.pprint(price)
        browser.quit()
        return price

    def scrape(self):
        if (regex.search(r'asos', self.url)):
            self.price = MainScraper.__getAsos(self.url)
        elif (regex.search(r'evomag', self.url)):
            self.price = MainScraper.__getEvomag(self.url)
        elif (regex.search(r'emag', self.url)):
            self.price = MainScraper.__getEmag(self.url, self.code)
        elif (regex.search(r'altex', self.url)):
            self.price = MainScraper.__getAltex(self.url)
        elif (regex.search(r'aoro', self.url)):
            self.price = MainScraper.__getAoro(self.url, self.code)
        elif (regex.search(r'cel', self.url)):
            self.price = MainScraper.__getCel(self.url)
        elif (regex.search(r'mobiledirect', self.url)):
            self.price = MainScraper.__getMobileDirect(self.url)
        elif (regex.search(r'quickmobile', self.url)):
            self.price = MainScraper.__getQuickmobile(self.url)
        elif (regex.search(r'amazon\.de', self.url)):
            self.price = MainScraper.__getAmazonDe(self.url)
        elif (regex.search(r'dualstore', self.url)):
            self.price = MainScraper.__getDualstore(self.url)


if __name__ == "__main__":
    product = dict(
        name='test',
        link='http://www.asos.com/adidas-originals/adidas-originals-tubular-rise-trainers-in-black-by3554/prd/8265765?clr=black&SearchQuery=&cid=1935&gridcolumn=2&gridrow=1&gridsize=4&pge=1&pgesize=72&totalstyles=2268'
    )
    scraper = MainScraper(product)
    try:
        scraper.scrape()
        scraper.show_scraper()
    except:
        print('Scraping error')
