import requests
from bs4 import BeautifulSoup

from Product import Product

matches = ["Ben", "Jerry", "465"]


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')


def supervalu():
    products = []
    soup = get_soup(
        "https://shop.supervalu.ie/shopping/search/allaisles?q=Ben%20%20Jerrys%20Ice%20Cream%20465%20ml&page=1")
    search_all = soup.find("div", id="search-all-aisles-listings-view")
    items = search_all.findAll("div", "col-xs-6")
    for item in items:
        name = str(item.find("h4").text)
        if all(x in name for x in matches):
            deal = str(item.find("div", class_="product-details-promotion-name").text)
            if not deal.isspace():
                products.append(Product(name.strip(), deal.strip(), "SuperValu"))

    return products


def tesco():
    products = []
    soup = get_soup(
        "https://www.tesco.ie/groceries/product/search/default.aspx?searchBox=ben&originalSearchTerm=freetext&Nao=0")
    product_list = soup.find("ul", class_="products")
    items = product_list.findAll("li")
    for item in items:
        if all(x in item.text for x in matches):
            deal = item.find("div", class_="promo")
            if deal:
                name = item.find("h3").text
                deal_str = " ".join((str(deal.text).replace('\r\n ', '')).split())
                products.append(Product(name, deal_str, "Tesco"))
    return products


if __name__ == '__main__':
    sv = supervalu()
    tsc = tesco()

    if sv:
        print("SuperValu:")
        for p in sv:
            print(f"\t{p.name}\n\t{p.deal}\n")

    if tsc:
        print("Tesco:")
        for p in tsc:
            print(f"\t{p.name}\n\t{p.deal}\n")
