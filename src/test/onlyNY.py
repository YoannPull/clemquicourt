import requests
import json
import webbrowser

website_url = "https://onlyny.com"
name_product = "NYC Varsity T-Shirt"
size_product = "L"
color = "Dark Green Heather"  # ou "Navy Heather"

with requests.Session() as s:
    # can help to avoid some trouble
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"{website_url}/"
    }) 
    r = s.get(f"{website_url}/products.json?limit=250") # to show more than thirthy articles
    r.raise_for_status()
    products = r.json().get("products", [])

    # on all the product of the site, find the product wanted
    product = next((p for p in products if p.get("title", "").strip() == name_product), None)
    if not product:
        raise ValueError(f"Didn't find the product: {name_product}")

    # Keep some info about the product (not needed)
    product_info = {
        "name_product": name_product,
        "id": product["id"],
        "handle": product["handle"],
        "variants": product["variants"]
    }

    # Find the variant ID of the product color and size
    variant = None
    for v in product_info["variants"]:
        # It's common to use option 1 and option 2. But it's better to do a manual check
        if str(v.get("option1", "")).strip().lower() == color.lower() and \
           str(v.get("option2", "")).strip().lower() == size_product.lower():   # we lower all the string to be more robust "à la casse".
            variant = v
            break

    # If they reverse the order between color and size
    if not variant:
        for v in product_info["variants"]:
            if str(v.get("option2", "")).strip().lower() == color.lower() and \
               str(v.get("option1", "")).strip().lower() == size_product.lower():
                variant = v
                break

    if not variant:
        raise ValueError(f"Didn't find the variant {name_product} → Color: {color}, Size: {size_product}")

    variant_id = variant["id"]
    print("Product :", product_info["handle"])
    print("Variant ID :", variant_id)

    # Not needed, URL of the product and variant
    url_product_size = f"{website_url}/products/{product_info['handle']}?variant={variant_id}"
    print("URL produit/variante :", url_product_size)

    # --- 2) Ajax flow cart : empty, add, go to the checkout ---
    # Empty the cart 
    s.post(f"{website_url}/cart/clear.js")

    # Add the variant into the cart
    add = s.post(f"{website_url}/cart/add.js", data={"id": variant_id, "quantity": 1})
    add.raise_for_status()
    print("Article added to the cart.")

    # Check the cart 
    cart = s.get(f"{website_url}/cart.json")
    cart.raise_for_status()
    cart_json = cart.json()
    print(f"Cart: {len(cart_json.get('items', []))} article(s)")

    # Go to the checkout and generate the URL : /checkouts/<token>. | To block bot, shopify generate token for each cart.
    checkout = s.get(f"{website_url}/checkout", allow_redirects=True) # generate a token
    checkout.raise_for_status()
    print("Checkout URL :", checkout.url)

    # Ouvrir dans le navigateur local
    webbrowser.open(checkout.url)
