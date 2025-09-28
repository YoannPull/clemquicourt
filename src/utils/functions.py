import requests
import json


def check_item():
    website_url = "https://clemquicourt.com"
    r = requests.get(f"{website_url}/products.json")
    products = json.loads((r.text))['products'] 
    # It seems that there is only one product, but just in case we are looking for this exact product
    product_wanted = "CLEM QUI COURT x BROOKS - ÉDITION LIMITÉE \"LA KILLCAM\""
    for product in products :
        if product["title"] == product_wanted:
            print(product["title"])
            product_url = f"{website_url}/products/{product['handle']}"

            return product_url
    return False
