from flask import Flask
import requests
from bs4 import BeautifulSoup

from Product import Product

app = Flask(__name__)

matches = ["Ben", "Jerry", "465"]


@app.route('/', methods=['GET'])
def promos():
    sites = {"SuperValu": supervalu(), "Tesco": tesco()}
    s = '''<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">'''
    s += "<h3>Current Ben and Jerry's Promotions</h3>"
    for site in sites:
        s += site + ":\n"
        s += "<ul style='list-style-type:none'>"
        for product in sites[site]:
            s += product.get_html()
        s += "</ul>"
    return s


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
        name = str(item.find("h4").text).strip()
        if all(x in name for x in matches):
            saving = item.find("div", class_="product-details-promotion-name").text
            if not saving.isspace():
                lifetime = " ".join(item.find("div", class_="product-details-promotion-lifetime").text.split())
                products.append(Product(
                    name=name,
                    saving=saving.strip(),
                    lifetime=lifetime,
                    link=item.find("a")['href'],
                    store="SuperValu")
                )

    return products


def tesco():
    products = []
    soup = get_soup(
        "https://www.tesco.ie/groceries/product/search/default.aspx?searchBox=ben&originalSearchTerm=freetext&Nao=0")
    product_list = soup.find("ul", class_="products")
    items = product_list.findAll("li")
    for item in items:
        if all(x in item.text for x in matches):
            promo = item.find("div", class_="promo")
            if promo:
                heading = item.find("h3")
                split = " ".join((str(promo.text).replace('\r\n ', '')).split()).split("valid")
                products.append(Product(
                    name=heading.text,
                    saving=split[0],
                    lifetime="Valid" + split[1],
                    link="https://www.tesco.ie" + heading.find("a")['href'],
                    store="Tesco")
                )

    return products


if __name__ == '__main__':
    app.run()
