from flask import Flask
import requests
from bs4 import BeautifulSoup

from Product import Product

app = Flask(__name__)

matches = ["Ben", "Jerry", "465"]


@app.route('/', methods=['GET'])
def promos():
    sites = {"SuperValu": supervalu(), "Tesco": tesco()}
    s = '''<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">'''
    s += "<div class='container-fluid'><h2>Ben and Jerry's Promotions</h2>" \

    for site in sites:
        s += f"</br><h2>{site}:</h2>\n"
        s += "<div class='d-grid gap-2'>"
        for product in sites[site]:
            s += product.get_html()
        s += "</div>"

    s += "</div>"
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
