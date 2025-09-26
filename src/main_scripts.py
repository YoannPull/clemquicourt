import requests
import json
from utils.functions import check_item

website_url = "https://clemquicourt.com"
r = requests.get(f"{website_url}/products.json")
products = json.loads((r.text))['products'] 
product = products[0]
print(product.keys())
print(product['variants'])
