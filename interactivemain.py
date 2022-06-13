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
        return False, None
    return True, soup.find(id="productTitle").getText().strip()


def below_price(url, price_you_want):
    if in_stock(url):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id="productTitle").getText().strip()
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
            return True, final_price, title
        return False, final_price, title
    return False, None, None


print("Enter 1 to get notified when item comes back in stock, enter 2 to get notified when item drops below a specific price, enter 3 if the item is out of stock and you want to be notified when it comes back in stock and is below a specific price: ")
choice = int(input())

url = input("Enter the url: ")

if choice == 1:
    while True:
        item_in_stock, title = in_stock(url)
        if item_in_stock:
            print(f"{title} is back in stock.")
            winsound.Beep(1500, 2000)
            break
        else:
            time.sleep(120)
elif choice == 2:
    price_you_want = int(input("Enter the desired price: "))
    while True:
        item_below_price, current_price, title = below_price(url, price_you_want)
        if item_below_price:
            print(f"{title} is below {price_you_want}. Current price: {current_price}")
            winsound.Beep(1500, 2000)
            break
        else:
            time.sleep(120)
elif choice == 3:
    price_you_want = int(input("Enter the desired price: "))
    while True:
        item_in_stock, title = in_stock(url)
        if item_in_stock:
            item_below_price, current_price, title = below_price(url, price_you_want)
            if item_below_price:
                print(f"{title} is below {price_you_want}. Current price: {current_price}")
                winsound.Beep(1500, 2000)
                break
            else:
                time.sleep(120)
        else:
            time.sleep(120)


