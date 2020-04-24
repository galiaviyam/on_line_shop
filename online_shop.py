# This is the main file to run the shop
from user import User
from store import Store
from product_list import ProductList
import pprint


def print_product_list(product_list):
    if not isinstance(product_list, ProductList):
        print("cant print non product list object")
        return
    for product in product_list.product_list:
        print("* " + product.name)

# main
#login to system
user = User(email="gali@mail", password="Aa123456")
session = user.login()

# get store home page
store = Store("MyShop")
store.get_store()
print("store homepage products:")
print_product_list(store.product_list)
print("------------------------")

# search
search = store.search("silver")
print("search results:")
print_product_list(search)
print("------------------------")

# get category
category = store.get_by_category(category="rings")
print("category rings:")
print_product_list(category)
print("------------------------")

# add to wishlist
add_to_wishlist = store.add_to_wishlist(email="gali@mail", sku="1003")
add_to_wishlist = store.add_to_wishlist(email="gali@mail", sku="1002")
add_to_wishlist = store.add_to_wishlist(email="gali@mail", sku="1004")
add_to_wishlist = store.add_to_wishlist(email="gali@mail", sku="1001")

# remove from wishlist
remove_from_wishlist = store.remove_from_wishlist(email="gali@mail", sku="1001")

# show wishlist
wishlist = store.show_wishlist(email="gali@mail")
print("wishlist:")
print_product_list(wishlist)
print("------------------------")

# add to cart
add_to_cart = store.add_to_cart(email="gali@mail", sku="1001")

# show cart
cart = store.show_cart(email="gali@mail")
print("cart:")
print_product_list(cart)
print("------------------------")

# checkout
checkout = store.checkout("gali@mail")

print("exit")