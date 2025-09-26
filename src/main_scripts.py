import requests
import json
from utils.functions import check_item

website_url = "https://clemquicourt.com"
r = requests.get(f"{website_url}/products.json")
products = json.loads((r.text))['products'] 
product = products[0]
print(product.keys())
print(product['variants'])



# # --- Config ---
# SHOP = "clemquicourt.com"  # domaine Shopify
# STOREFRONT_TOKEN = "shpua_..."  # Storefront Access Token à mettre dans tes secrets

# producturl = check_item()
# print("Produit choisi :", producturl)

# # Ici il faudrait résoudre l’ID de variante à partir de l’URL.
# # Exemple : tu as déjà trouvé que c’est "gid://shopify/ProductVariant/1234567890"
# variant_gid = "gid://shopify/ProductVariant/1234567890"

# # --- 2. Mutation GraphQL pour créer un panier ---
# graphql = """
# mutation ($lines: [CartLineInput!]!) {
#   cartCreate(input: { lines: $lines }) {
#     cart { id checkoutUrl totalQuantity }
#     userErrors { field message }
#   }
# }
# """

# variables = {
#     "lines": [
#         {"quantity": 1, "merchandiseId": variant_gid}
#     ]
# }

# # --- 3. Appel API Shopify ---
# try:
#     r = requests.post(
#         f"https://{SHOP}/api/2024-10/graphql.json",
#         headers={
#             "X-Shopify-Storefront-Access-Token": STOREFRONT_TOKEN,
#             "Content-Type": "application/json",
#         },
#         json={"query": graphql, "variables": variables},
#         timeout=20
#     )
#     r.raise_for_status()
#     data = r.json()
# except requests.RequestException as e:
#     raise SystemExit(f"Erreur réseau/HTTP : {e}")
# except ValueError:
#     raise SystemExit(f"Réponse non JSON : {r.text[:200]}")

# # --- 4. Vérification des erreurs ---
# errors = data.get("errors")
# user_errors = (data.get("data", {})
#                  .get("cartCreate", {})
#                  .get("userErrors", []))

# if errors:
#     raise SystemExit(f"Erreurs GraphQL : {errors}")

# if user_errors:
#     msgs = "; ".join(e.get("message", "Erreur inconnue") for e in user_errors)
#     raise SystemExit(f"Erreurs côté Shopify : {msgs}")

# # --- 5. Récupération du checkoutUrl ---
# cart = data.get("data", {}).get("cartCreate", {}).get("cart")
# if not cart or not cart.get("checkoutUrl"):
#     raise SystemExit(f"Cart introuvable dans la réponse : {json.dumps(data, indent=2)}")

# print("Ouvre le checkout :", cart["checkoutUrl"])
