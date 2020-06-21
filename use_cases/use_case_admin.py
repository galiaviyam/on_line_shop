# This is the main file to run the shop as an admin
from store import Store
from user import User

# main
store = Store("config.json")
store.get_store()

# login
user = User("admin@mail", store.session_id)
print("login:")
if not user.login("admin@mail", password="Administrator!"):
    print("password is incorrect")
else:
    print("welcome %s" % user.name)
print("------------------------")

# change password - possible for every user
print("change password:")
if not user.change_password("admin@mail", "Administrator!", "Administrator!!"):
    print("There was a problem")
else:
    print("Password changed successfully")
print("------------------------")

# create seller
print("Create new seller:")
success_user = store.add_user(email="new_seller@mail", password="Aa123456", type="seller")
if not success_user:
    print(store.error)
else:
    print("Seller created successfully")
print("------------------------")
