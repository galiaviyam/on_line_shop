# This is the main file to run the shop as a seller
from store import Store
from user import User


def print_product_list(product_list):
    if not isinstance(product_list, list):
        print("cant print non product list object")
        return
    for product in product_list:
        print("* " + product.name)

# main

store = Store("MyShop")
store.get_store()

#login to system
user = User("seller@mail", store.session_id)
print("login:")
if not user.login("seller@mail", password="Aa123456"):
    print("password is incorrect")
else:
    print("welcome %s" % user.name)
print("------------------------")

# add product
print("add product")
new_products = [("1001", "gold ring", 355, "0", "description", "gold", "yellow", "5", "rings", 1),
                ("1002", "silver necklace", 199, "10", "description", "silver", "silver", "50cm", "necklaces", 0),
                ("1003", "hoop earrings", 329, "15", "description", "silver", "silver", "2", "earrings", 1),
                ("1004", "stud earrings", 299, "0", "description", "gold", "white", "1", "earrings", 0),
                ("1005", "copper bracelet", 105, "20", "description", "copper", "red", "OS", "bracelets", 1),
                ("1006", "pearl necklace", 219, "0", "description", "silver", "silver", "45cm", "necklaces", 0),
                ("1007", "pearl earrings", 300, "10", "description", "gold", "yellow", "OS", "earrings", 0),
                ("1008", "pearl bracelet", 259, "0", "description", "gold", "rose", "OS", "bracelets", 1)]
for product in new_products:
    new_product = store.add_product(*product)
    if new_product is None:
        print(store.error)
    else:
        print(new_product.print())
print("------------------------")

# modify product
print("modify product")
product = store.modify_product("1007", price=176)
if product is None:
    print(store.error)
else:
    print(product.print())
print("------------------------")

# delete product
print("delete product")
product_to_delete = store.delete_product("1007")
if product_to_delete is None:
    print(store.error)
else:
    print(product_to_delete.print())
print("------------------------")

# show orders
store.show_orders()
