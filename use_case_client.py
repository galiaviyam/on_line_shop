# This is the main file to run the shop as a client
from user import User
from store import Store


def print_product_list(product_list):
    if not isinstance(product_list, list):
        print("cant print non product list object")
        return
    for product in product_list:
        print("* " + product.name)

# main
# get store home page
store = Store("MyShop")
store.get_store()

print("store homepage products:")
print_product_list(store.product_list)
print("------------------------")

#create new user
print("new user:")
success_user = store.add_user(email="client@mail", password="Aa123456")
if not success_user:
    print(store.error)
else:
    print("Welcome, Please log in!")
print("------------------------")

# login to system - fail
user = User("client@mail", store.session_id)
print("login:")
if not user.login("client@mail", password="Aa12346"):
    print("Password or username is incorrect")
else:
    print("Welcome %s" % user.name)
print("------------------------")

# login to system - success
print("login:")
if not user.login("client@mail", password="Aa123456"):
    print("password is incorrect")
else:
    print("welcome %s" % user.name)
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
user.add_to_wishlist(email="client@mail", sku="1003")
user.add_to_wishlist(email="client@mail", sku="1002")
user.add_to_wishlist(email="client@mail", sku="1004")
user.add_to_wishlist(email="client@mail", sku="1001")

# remove from wishlist
remove_from_wishlist = user.remove_from_wishlist(email="client@mail", sku="1001")

# show wishlist
wishlist = user.show_wishlist(email="client@mail")
print("wishlist:")
print_product_list(wishlist)
print("------------------------")

# add to cart
user.add_to_cart(email="client@mail", sku="1001")
user.add_to_cart(email="client@mail", sku="1002")
user.add_to_cart(email="client@mail", sku="1003")

# remove from cart
remove_from_cart = user.remove_from_cart(email="client@mail", sku="1002")

# show cart
(cart, total_price) = user.show_cart(email="client@mail")
print("cart:")
print_product_list(cart)
print("total price: " + str(total_price))
print("------------------------")

# checkout
checkout = user.checkout("client@mail")

print("exit")