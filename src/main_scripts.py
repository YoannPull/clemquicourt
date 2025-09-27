import requests
import json
import webbrowser

website_url = "https://clemquicourt.com"

# 1) Fetch a product and get the variant "L"
r = requests.get(f"{website_url}/products.json")
r.raise_for_status()  # raises an exception if the request fails (HTTP error)
products = r.json()["products"]  # extract product list from JSON
product = products[0]  # just take the first product for the example

product_size = "L"
variant_id = None
# Search for the variant with the given size (e.g. "L")
for v in product["variants"]:
    if v["title"] == product_size:
        variant_id = v["id"]
        break
# Make sure the variant was found, otherwise raise an error
assert variant_id, f"Variant {product_size} not found on {product['handle']}"

# Build the product URL including the variant
url_product_size = f"{website_url}/products/{product['handle']}?variant={variant_id}"
print("Product/variant URL:", url_product_size)

# 2) Create a session, add the item to the cart, and go to checkout
with requests.Session() as s:
    # Set a User-Agent to mimic a real browser
    s.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Safari/537.36"

    # (Optional) Empty the cart before adding the new item
    s.post(f"{website_url}/cart/clear.js")

    # Add the selected variant to the cart
    add = s.post(f"{website_url}/cart/add.js", data={"id": variant_id, "quantity": 1})
    add.raise_for_status()
    print("Item added to cart.")

    # Request the checkout page (this will redirect to a tokenized URL)
    checkout = s.get(f"{website_url}/checkout", allow_redirects=True)
    checkout.raise_for_status()

    # The final checkout URL looks like /checkouts/<token>
    print("Checkout URL:", checkout.url)

    # Open the checkout page in your local browser (safe to test without payment)
    webbrowser.open(checkout.url)
