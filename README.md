# storey
This projects is a backend of an on-line shop. The shop provides product search using categories and search bar, adding products to wish-list and shopping-cart, seller management (adding, removing and editing products and tracking of orders).
The data is stored in a Database, using sqlite3.
This product can create new stores and use them. In order to do that there are two things you need to do:
1. modify the config.json file and change the values inside according to the new store you want store name, database name, and timeout in seconds (default 3600)
2. run the database.py file with the flag: --db_name < NAME > 

In order to run the project, there are dependencies in the requirements.txt file.
run this line:
pip install -r requirements.txt

There are three user interfaces - one for clients, one for sellers and one for admin.
 