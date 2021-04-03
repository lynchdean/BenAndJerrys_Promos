import requests
from bs4 import BeautifulSoup
from flask import Flask

from Product import Product

app = Flask(__name__)

matches = ["Ben", "Jerry", "465"]


@app.route('/', methods=['GET'])
def promos():
    sites = {"SuperValu": supervalu(), "Tesco": tesco()}
    first = True
    titles = []
    content = []
    for site in sites:
        titles.append(
            f'<button class="nav-link {"active" if first else ""}" id="nav-{site.lower()}-tab" data-bs-toggle="tab" '
            f'data-bs-target="#nav-{site.lower()}" type="button" role="tab" aria-controls="nav-{site.lower()}" '
            f'aria-selected="true"><h1>{site}</h1></button>')

        content.append(f'<div class="tab-pane fade {"show active" if first else ""}" id="nav-{site.lower()}" '
                       f'role="tabpanel" aria-labelledby="nav-{site.lower()}-tab">')
        content.append('<div class="d-grid gap-2 my-2">')
        for product in sites[site]:
            content.append(product.get_card())
        content.append('</div>')
        content.append('</div>')
        first = False
    return build_page(titles, content)


def build_page(titles, content):
    bootstrap = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">' \
                '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>'
    title = '<div class="container-fluid"><div class="text-center"><h1 class="display-2">Ben and Jerry\'s Promotions</h1></div>'
    tabs = f'<nav><div class="nav nav-pills" id="nav-tab" role="tablist">{"".join(titles)}</div>'
    content = f'<div class="tab-content" id="nav-tabContent">{"".join(content)}</div>'

    return bootstrap + title + tabs + content


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
