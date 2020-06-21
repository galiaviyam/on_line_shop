# This is the file to run the shop as a admin
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
        if user_type == "admin":
            print("welcome %s" % store.user.name)
            homepage()
        else:
            print("You do not have permission")
            sys.exit(1)


def homepage():
    choice = input("What would you like to do? Please type the number:\n1. See all clients\n2. See all sellers\n"
                   "3. Create a seller\n4. Exit\n--->")
    if choice == "1":  # See all clients
        show_users("client")
        homepage()
    elif choice == "2":  # See all sellers
        show_users("seller")
        homepage()
    elif choice == "3":  # Create a seller
        create_seller()
        homepage()
    elif choice == "4":  # exit
        print("See you next time :)")
        sys.exit()
    else:
        print("Please enter a valid choice")
        homepage()


def show_users(user_type):
    users = store.get_users(user_type)
    page_limit = 3
    if users:
        headers = ["name", "email", "country", "city", "street", "house_num", "apartment", "entrance", "zip_code",
                   "phone"]
        table = []
        for num in range(len(users)):
            table.append([users[num]["name"], users[num]["email"], users[num]["country"], users[num]["city"],
                          users[num]["street"], users[num]["house_num"], users[num]["apartment"],
                          users[num]["entrance"], users[num]["zip_code"], users[num]["phone"]])
            if (num + 1) % page_limit == 0 or (num + 1) == len(users):
                print(user_type + "s:")
                print(tabulate(table, headers, tablefmt="grid"))
                table = []
                print("")
                if num + 1 < len(users):
                    input("press enter for next page")


def create_seller():
    email = input("email: ")
    password = input("password: ")
    name = input("full name: ")
    user_type = "seller"
    country = input("country: ")
    city = input("city: ")
    street = input("street: ")
    house_num = input("house number: ")
    apartment = input("apartment: ")
    entrance = input("entrance: ")
    zip_code = input("zip code: ")
    phone = input("phone: ")
    success_user = store.add_user(email, password, name, user_type, country, city, street, house_num, apartment,
                                  entrance, zip_code, phone)
    if not success_user:
        print(store.error)
    else:
        print("Seller created successfully!")


if __name__ == "__main__":
    store = Store("config.json")
    store.get_store()
    print("Welcome to %s!" % store.name)
    login()
