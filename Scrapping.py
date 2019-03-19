from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import lxml
import re
import requests
import sys


"""
Function To Scrap Individual Item
"""

def get_details(soup):
    title = soup.find('span', id="productTitle")
    price = soup.find('span', id="priceblock_ourprice")
    availablity = soup.find('div', id="availability")
    str = ""
    if price is not None:
        for line in price.stripped_strings :
            str = line
        str = str.replace(",","")
    else:
        price = soup.find('span', id="priceblock_saleprice")
        for line in price.stripped_strings :
            str = line
        str = str.replace(",","")
    price = str
    try:
        print(title.get_text(),price,availablity.get_text())
    except:
        print("Invalid URL..............")
        return

"""
Class For Scrapping Amazon Website
"""

class AmazonScrapper:

    def __init__(self):
        self.asin = list()
        self.url = str()

    def get_url(self):
        """
        Get Main Page URL
        """
        pro = " ".join(map(str,(list(sys.argv)[1:])))
        # print(pro)
        # pro = input("Enter the Product to Be Searched:")
        product = pro.split(sep=' ')
        product = "+".join(map(str,product))
        self.url = "https://www.amazon.in/s?k=" + str(product)

    def ret_list_of_asin_code(self):
        """
        Get Individual Item ASIN Code
        """
        print("Opening URL " + str(self.url))
        source = urlopen(Request(self.url, headers={'User-Agent': 'Mozilla'})).read()
        soup = BeautifulSoup(source,features="lxml")
        self.asin = set(re.findall("(?:[/dp/]|$)([A-Z0-9]{10})",str(soup.prettify())))
        self.asin = list(self.asin)
        temp = [i for i in self.asin if i.startswith('B')]
        self.asin = temp
        #print(self.asin)    #list of Asin Codes

    def opening_url_on_asin(self):
        """
        Opening Individual Item Page
        """
        for i in self.asin:
            try:
                url = str("https://www.amazon.in/dp/")+str(i)
                print("Processing " + str(url))
                src = urlopen(Request(url, headers={'User-Agent': 'Mozilla'})).read()
                soup = BeautifulSoup(src,features="lxml")
                get_details(soup)
            except:
                continue

"""
Class For Login Into Amazon Server (Client to Server)
"""

class SocketProgramming:

    def __init__(self):
        self.session = requests.Session()
        self.url = str()
        self.data = dict()

    def verification(self):
        """
        Verification of Email and Password at Server
        """
        post_resp = self.session.post("https://www.amazon.com/ap/signin",data = self.data)
        post_soup = BeautifulSoup(post_resp.content,"lxml")
        if post_soup.find_all('title')[0].text == 'Your Account':
            print('Login Successfull')
        else:
            print('Login Unsuccessfull')
        self.session.close()

    def socket_programming(self):
        """
        Initiating Socket Programming Client to Server
        """
        self.url = "https://www.amazon.com/gp/sign-in.html"
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.61 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': self.url
        }
        resp = self.session.get(self.url)
        source = resp.text
        soup = BeautifulSoup(source,"lxml")
        form = soup.find('form',{'name':'signIn'})
        for col in form.find_all('input'):
            try:
                self.data[col['name']] = col['value']
            except:
                pass
        self.data[u'email'] = input('Enter the Username:')
        self.data[u'password'] = input('Enter the Password:')




if __name__=="__main__":
    s = SocketProgramming()
    s.socket_programming()
    s.verification()
    a = AmazonScrapper()
    a.get_url()
    a.ret_list_of_asin_code()
    a.opening_url_on_asin()
