import time

import requests
import winsound
from bs4 import BeautifulSoup


def is_number(s):
    if s == '0' or s == '1' or s == '2' or s == '3' or s == '4' or s == '5' or s == '6' or s == '7' or s == '8' or s == '9' or s == '.':
        return True
    return False


def in_stock(url):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    stock = soup.find(id="availability").getText().strip()
    if stock == "Currently unavailable.    We don't know when or if this item will be back in stock.":
        return False
    return True


def below_price(url, price_you_want):
    if in_stock(url):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id="productTitle").getText()
        # price = soup.find(id="apex_desktop")
        spans = soup.find_all('span', {'class': 'a-price-whole'})

        #print(spans)

        price = str(spans[0])
        final_price = ""
        for s in price:
            if is_number(s):
                final_price += s

        final_price = float(final_price)
        if final_price <= price_you_want:
            return True
        return False
    return False


url = "https://www.amazon.in/HP-X1000-Wired-Mouse-Black/dp/B009VCGPSY/?_encoding=UTF8&pd_rd_w=trVfK&content-id=amzn1.sym.80ce8153-3c1f-484b-945b-e784d0727fa9&pf_rd_p=80ce8153-3c1f-484b-945b-e784d0727fa9&pf_rd_r=7P5WN4W4YQ3KYRJ02GGT&pd_rd_wg=kld64&pd_rd_r=397a4ff1-e7bc-412b-b48d-b0cd5fa2b19c&ref_=pd_gw_crs_zg_bs_976392031"
price = 260

while True:
    price_is_below = below_price(url, price)
    print("checking...")
    if not price_is_below:
        print("not below")
        time.sleep(120)
        continue
    else:
        print("The product has dropped in price")
        winsound.Beep(1500, 2000)
        break