# This is the file to run the shop as a client
from store import Store
from tabulate import tabulate
import sys


def homepage():
    show_products(store.product_list, "home")
    actions()


def actions():
    choice = input("What would you like to do? Please type the number:\n1. Log in or sign in\n2. Search\n"
                   "3. Go to category\n4. Show one product\n5. Show cart\n6. Show wishlist\n7. Exit\n--->")
    if choice == "1":  # Log in or sign in
        user_actions()
    elif choice == "2":  # Search
        search()
    elif choice == "3":  # Go to category
        search_category()
    elif choice == "4":  # Show one product
        sku = input("sku:__")
        if show_one_product(sku) == 1:
            print("A product with SKU %s does not exist" % sku)
            actions()
    elif choice == "5":  # show cart
        show_cart()
    elif choice == "6":  # show wishlist:
        show_products(store.user.show_wishlist(), "wishlist")
    elif choice == "7":  # exit
        print("See you next time :)")
        sys.exit()
    else:
        print("Please enter a valid choice")
        actions()


def user_actions():
    choice = input("What would you like to do? Please type the number:\n1. Log in\n2. sign in\n"
                   "3. change password\n4. return to homepage--->")
    if choice == "1":  # log in
        login()
    elif choice == "2":  # sign in
        new_user()
    elif choice == "3":  # change password
        email = input("please enter your email: ")
        old_password = input("please enter your old password: ")
        new_password = input("please enter your new password: ")
        if store.user.change_password(email, old_password, new_password):
            print("password changed successfully! please log in:")
            login()
    elif choice == "4":  # return to homepage
        homepage()
    else:
        print("Please enter a valid choice")
        user_actions()


def search():
    search_input = input("search: ")
    results = store.search(search_input)
    show_products(results, "search results")
    products_actions()


def show_categories():
    categories = store.get_categories()
    print("store categories:")
    for category in categories:
        print("* " + category['category'])


def search_category():
    show_categories()
    choice = input("Please type category--->")
    category = store.get_by_category(category=choice)
    show_products(category, "category")
    products_actions()


def show_products(product_list, list_type):
    if product_list:
        headers = ["sku", "name", "price", "discount %", "final_price", "description", "material", "color", "size"]
        table = []
        for product in product_list:
            table.append([product.sku, product.name, product.price, product.discount, product.final_price,
                          product.description, product.material, product.color, product.size])
        print(tabulate(table, headers, tablefmt="grid"))
        print("")
    else:
        print(list_type + " is empty")
        actions()


def products_actions():
    choice = input("What would you like to do? Please type the number:\n1. show one product\n"
                   "2. return to homepage\n--->")
    if choice == "1":  # show one product
        sku = input("Please enter sku:__")
        if show_one_product(sku) == 1:
            print("A product with SKU %s does not exist" % sku)
            products_actions()
    elif choice == "2":  # return to homepage
        homepage()
    else:
        print("Please enter a valid choice")
        products_actions()


def show_cart():
    print("cart:")
    show_products(store.user.show_cart()[0], "cart")
    print("Total price: " + str(store.user.show_cart()[1]))
    choice = input("What would you like to do? Please type the number:\n1. remove product\n2. checkout\n"
                   "3. return to homepage\n--->")
    if choice == "1":  # remove product
        sku_to_remove = input("please type the sku you want to remove from the cart:--->")
        remove = store.user.remove_from_cart(sku_to_remove)
        if remove:
            print("product removed from cart")
    elif choice == "2":  # checkout
        checkout()
    elif choice == "3":  # return to homepage
        homepage()
    else:
        print("Please enter a valid choice")
        show_cart()


def checkout():
    checkout_result = store.user.checkout()
    if checkout_result == 0:
        print("Thank you for shopping")
    elif checkout_result == 2:
        print("Please log in")
        user_actions()
    elif checkout_result == 1:
        print("There was an error")


def show_wishlist():
    print("wishlist:")
    show_products(store.user.show_wishlist(), "wishlist")
    choice = input("What would you like to do? Please type the number:\n1. remove product\n2. move product to cart"
                   "\n3. return to homepage\n--->")
    if choice == "1":  # remove product
        sku_to_remove = input("please type the sku you want to remove from wishlist:--->")
        remove = store.user.remove_from_wishlist(sku_to_remove)
        if remove:
            print("product removed from cart")
    elif choice == "2":  # move to cart
        sku = input("please enter sku: ")
        action = store.user.add_to_cart(sku)
        remove = store.user.remove_from_wishlist(sku)
        if action:
            print("Item moved to cart")
    elif choice == "3":  # return to homepage
        homepage()
    else:
        print("Please enter a valid choice")
        show_wishlist()


def show_one_product(sku):
    db_filter = {"sku": sku}
    result = store.db.get_record("products", db_filter)
    if int(sku) not in result.values():
        return 1
    headers = ["sku", "name", "price", "discount %", "final_price", "description", "material", "color", "size"]
    table = [[str(result["sku"]), result["name"], str(result["price"]), str(result["discount"]),
              str(result["final_price"]), result["description"], result["material"], result["color"], result["size"]]]
    print(tabulate(table, headers, tablefmt="grid"))
    print("")
    choice = input("1. add to cart\n2. add to wishlist\n3. return to home page\n--->")
    if choice == "1":  # add to cart
        action = store.user.add_to_cart(sku)
        if action:
            print("Item added to cart")
            show_cart()
    elif choice == "2":  # add to wishlist
        action = store.user.add_to_wishlist(sku)
        if action:
            print("Item added to wishlist")
            show_wishlist()
    elif choice == "3":  # return to homepage
        homepage()
    else:
        print("Please enter a valid choice")
        if show_one_product(sku) == 1:
            print("A product with SKU %s does not exist" % sku)


def login(attempt=1):
    if attempt > 3:
        print("Too many attempts.")
        sys.exit(1)
    print("login:")
    email = input("email:--->")
    password = input("password:--->")
    if not store.user.login(email, password):
        attempt += 1
        print("password is incorrect")
        login(attempt)
    else:
        print("welcome %s" % store.user.name)
        homepage()


def new_user():
    email = input("email: ")
    password = input("password: ")
    name = input("full name: ")
    user_type = "client"
    country = input("country: ")
    city = input("city: ")
    street = input("street: ")
    house_num = input("house number: ")
    apartment = input("apartment: ")
    entrance = input("entrance: ")
    zip_code = input("zip code: ")
    phone = input("phone: ")
    success_user = store.add_user(email, password, name, user_type, country, city, street, house_num, apartment, entrance, zip_code
                                  , phone)
    if not success_user:
        print(store.error)
    else:
        print("Welcome, Please log in!")
        login()


if __name__ == "__main__":
    store = Store("config.json")
    store.get_store()
    print("Welcome to %s!" % store.name)
    homepage()

