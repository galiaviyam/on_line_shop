# This is the file to run the shop as a seller
from store import Store
from tabulate import tabulate
import sys


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
        user_type = store.user.get_user_type()
        if user_type == "seller" or user_type == "admin":
            print("welcome %s" % store.user.name)
            homepage()
        else:
            print("You do not have permission")
            sys.exit(1)


def homepage():
    choice = input("What would you like to do? Please type the number:\n1. Search\n2. Go to category\n3. Add product\n"
                   "4. Add category\n5. Show one product\n6. Show orders\n7. Exit\n--->")
    if choice == "1":  # search
        search()
        homepage()
    elif choice == "2":  # Go to category
        search_category()
    elif choice == "3":  # add product
        add_product()
    elif choice == "4":  # Add category
        add_category()
        homepage()
    elif choice == "5":  # Show one product
        sku = input("sku:__")
        if show_one_product(sku) == 1:
            print("A product with SKU %s does not exist" % sku)
            homepage()
    elif choice == "6":  # Show orders
        show_orders()
    elif choice == "7":  # Exit
        print("See you next time :)")
        sys.exit()
    else:
        print("Please enter a valid choice")
        homepage()


def search():
    search_input = input("search: ")
    results = store.search(search_input)
    show_products(results)


def show_categories():
    categories = store.get_categories()
    print("store categories:")
    for category in categories:
        print("* " + category['category'])


def search_category():
    show_categories()
    choice = input("Please type category--->")
    category = store.get_by_category(category=choice)
    show_products(category)
    homepage()


def add_product():
    sku = input("sku:__")
    name = input("name:__")
    price = input("price:__")
    while not price.isnumeric():
        print("Price must be a number!")
        price = input("price:__")
    discount = input("discount percent:__")
    while not discount.isnumeric() and discount != "":
        print("Discount must be a number!")
        price = input("discount:__")
    description = input("description:__")
    material = input("material:__")
    color = input("color:__")
    size = input("size:__")
    show_categories()
    category = input("category:__")
    is_homepage = input("Do you want this product to appear on homepage?(yes or no):__")
    if is_homepage == "yes":
        is_homepage = 1
    else:
        is_homepage = 0
    new_product = store.add_product(sku, name, price, discount, description, material, color, size, category,
                                    is_homepage)
    if new_product:
        print("Product added successfully!")
        show_one_product(sku)


def show_products(product_list):
    if product_list:
        headers = ["sku", "name", "price", "discount %", "final_price", "description", "material", "color", "size"]
        table = []
        for product in product_list:
            table.append([product.sku, product.name, product.price, product.discount, product.final_price,
                          product.description, product.material, product.color, product.size])
        print(tabulate(table, headers, tablefmt="grid"))
        print("")
    else:
        print("list is empty")
        homepage()


def show_one_product(sku):
    db_filter = {"sku": sku}
    result = store.db.get_record("products", db_filter)
    if sku not in result:
        return 1
    headers = ["sku", "name", "price", "discount %", "final_price", "description", "material", "color", "size"]
    table = [[str(result["sku"]), result["name"], str(result["price"]), str(result["discount"]),
              str(result["final_price"]), result["description"], result["material"], result["color"], result["size"]]]
    print(tabulate(table, headers, tablefmt="grid"))
    print("")
    choice = input("1. modify product\n2. delete product\n3. return to home page\n--->")
    if choice == "1":  # modify product
        modify_product(sku)
    elif choice == "2":  # delete product
        delete_product(sku)
        homepage()
    elif choice == "3":  # return to homepage
        homepage()
    else:
        print("Please enter a valid choice")
        show_one_product(sku)
    return 0


def modify_product(sku):
    name = input("name:__")
    price = input("price:__")
    while not price.isnumeric():
        print("Price must be a number!")
        price = input("price:__")
    discount = input("discount:__")
    while not discount.isnumeric() and discount != "":
        print("Discount must be a number!")
        price = input("discount:__")
    description = input("description:__")
    is_homepage = input("Do you want this product to appear on homepage?(yes or no):__")
    action = store.modify_product(sku, name=name, price=price, discount=discount, description=description,
                                  homepage=is_homepage)
    if action:
        print("Product modified successfully")
    show_one_product(sku)


def delete_product(sku):
    action = store.delete_product(sku)
    return action


def show_orders():
    print("orders:")
    store.show_orders()
    homepage()


def add_category():
    show_categories()
    new_category = input("Please type new category:__")
    store.add_category(new_category)
    print("category added successfully")
    show_categories()



if __name__ == "__main__":
    store = Store("config.json")
    store.get_store()
    print("Welcome to %s!" % store.name)
    login()
