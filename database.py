import time


class Database(object):
    def __init__(self, db_name):
        self.db_name = db_name

    @staticmethod
    def add_record(table_name, columns):
        if table_name == "sessions":
            columns["email"] = "gali@mail"
            columns["id"] = "1"
            columns["timestamp"] = time.time()
            return columns
        if table_name == "carts":
            columns["email"] = "gali@mail"
            columns["sku"] = "1001"
            return columns
        return None

    def create_record(self):
        pass

    def modify_record(self):
        pass

    @staticmethod
    def get_record(table_name, columns):
        results = {}
        if table_name == "users":
            if columns["email"] == "gali@mail" and columns["password"] == "Aa123456":
                results["name"] = "gali"
                return results
        if table_name == "stores":
            results["name"] = "MyShop"
            results["terms"] = "These are the terms of the shop: bla bla bla"
            return results
        if table_name == "products":
            results["sku"] = "1001"
            results["name"] = "gold ring"
            results["price"] = 129
            return results
        return None


    @staticmethod
    def get_records(table_name, columns):
        results = {}
        if table_name == "categories":
            results["sale"] = {}
            results["necklaces"] = {}
            results["rings"] = {}
            results["earrings"] = {}
            results["bracelets"] = {}
            return results
        if table_name == "products":
            try:
                if columns["homepage"] == "1":
                    results["1001"] = {"name": "gold ring", "price": 129}
                    results["1002"] = {"name": "silver necklace", "price": 234}
                    results["1003"] = {"name": "hoop earrings", "price": 325}
                    return results
            except KeyError:
                pass
            try:
                if columns["category"] == "rings":
                    results["1001"] = {"name": "gold ring", "price": 129}
                    return results
            except KeyError:
                pass
        if table_name == "carts":
            try:
                #if columns["email"] == "gali@mail":
                results["2"] = {"email": "gali@mail", "sku": "1001"}
                return results
            except KeyError:
                pass

        return None

    @staticmethod
    def search(table_name, columns):
        pass

    # This method will delete the selected records from the DB, but at this point there is no DB yet.
    @staticmethod
    def delete_record(table_name, columns):
        pass
