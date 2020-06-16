import sqlite3
from argparse import ArgumentParser
import sys
from urllib.request import pathname2url


class DatabaseException(Exception):
    pass


class Database(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.dburi = 'file:{}?mode=rw'.format(pathname2url(self.db_name))
        self.connection = None
        self.cursor = None

    def add_record(self, table_name, columns):
        column_names = ""
        values = ""
        for key, value in columns.items():
            column_names += key + ','
            values += "\"" + str(value) + "\"" + ','
        column_names = column_names.rstrip(',')
        values = values.rstrip(',')
        sql = "INSERT INTO %s (%s) VALUES( %s);" % (table_name, column_names, values)
        with sqlite3.connect(self.dburi, uri=True) as connection:
            self.cursor = connection.cursor()
            self.cursor.execute(sql)
            connection.commit()
        return self.get_record(table_name, columns)

    def modify_record(self, table_name, columns, new_values):
        where = "WHERE "
        for key, value in columns.items():
            where += "%s = \"%s\" AND " % (key, value)
        where = where[:-5]
        set = "SET "
        for key, value in new_values.items():
            set += "%s = \"%s\", " % (key, value)
        set = set[:-2]
        sql = "UPDATE %s %s %s" % (table_name, set, where)
        with sqlite3.connect(self.dburi, uri=True) as connection:
            self.cursor = connection.cursor()
            self.cursor.execute(sql)
            connection.commit()
        columns.update(new_values)
        return self.get_record(table_name, columns)

    def get_record(self, table_name, columns):
        where = "WHERE "
        for key, value in columns.items():
            where += "%s = \"%s\" AND " % (key, value)
        where = where[:-5]
        sql = "SELECT * FROM %s %s" % (table_name, where)
        with sqlite3.connect(self.dburi, uri=True) as connection:
            self.cursor = connection.cursor()
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            results = {}
            if row is None:
                return results
            for iter in range(len(row)):
                results[self.cursor.description[iter][0]] = row[iter]
        return results

    def get_records(self, table_name, columns):
        where = "WHERE "
        for key, value in columns.items():
            where += "%s = \"%s\" AND " % (key, value)
        where = where[:-5]
        sql = "SELECT * FROM %s %s" % (table_name, where)
        with sqlite3.connect(self.dburi, uri=True) as connection:
            self.cursor = connection.cursor()
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            results = {}
            uid = 0
            for row in rows:
                result = {}
                for iter in range(len(row)):
                    result[self.cursor.description[iter][0]] = row[iter]
                results[uid] = result
                uid += 1
        return results

    # columns is a list of tuples, containing key, value and compare operator
    def search(self, table_name, columns):
        where = "WHERE "
        for key, value, operator in columns:
            if operator in ["=", "<>", "!=", ">", "<", "<=", ">="]:
                if not value.isnumeric():
                    value = "\"%s\"" % value
                where += "%s %s %s OR " % (key, operator, value)
            if operator == "LIKE":
                where += key + " LIKE \"%" + value + "%\" OR "
        where = where[:-4]
        sql = "SELECT * FROM %s %s" % (table_name, where)
        with sqlite3.connect(self.dburi, uri=True) as connection:
            self.cursor = connection.cursor()
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            results = {}
            uid = 0
            for row in rows:
                result = {}
                for iter in range(len(row)):
                    result[self.cursor.description[iter][0]] = row[iter]
                results[uid] = result
                uid += 1
        return results

    # This method will delete the selected records from the DB, but at this point there is no DB yet.

    def delete_record(self, table_name, columns):
        where = "WHERE "
        for key, value in columns.items():
            where += "%s = \"%s\" AND " % (key, value)
        where = where[:-5]
        sql = "DELETE FROM %s %s" % (table_name, where)
        with sqlite3.connect(self.dburi, uri=True) as connection:
            self.cursor = connection.cursor()
            self.cursor.execute(sql)
            connection.commit()

    def get_next_number(self, table_name, column_name):
        sql = "select max(%s) + 1 from %s" % (column_name, table_name)
        with sqlite3.connect(self.dburi, uri=True) as connection:
            self.cursor = connection.cursor()
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
        if row[0] is None:
            return 1
        return row[0]

    def connect(self, new_db=None):
        if new_db is None:
            try:
                self.dburi = 'file:{}?mode=rw'.format(pathname2url(self.db_name))
                #self.connection = sqlite3.connect(self.dburi, uri=True)
            except sqlite3.OperationalError:
                raise DatabaseException()
        else:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def create_database(self, password):
        try:
            self.cursor.execute("""CREATE TABLE "carts" (
                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                "email"	TEXT NOT NULL,
                "sku"	NUMERIC NOT NULL
            );""")
        except:
            pass
        try:
            self.cursor.execute("""CREATE TABLE "wishlist" (
                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                "email"	TEXT NOT NULL,
                "sku"	NUMERIC NOT NULL
            );""")
        except:
            pass
        try:
            self.cursor.execute("""CREATE TABLE "categories" (
                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                "category"	TEXT NOT NULL,
                "description"	TEXT
            );""")
        except:
            pass
        try:
            self.cursor.execute("""CREATE TABLE "products" (
                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                "sku"	NUMERIC NOT NULL UNIQUE,
                "name"	TEXT NOT NULL,
                "category"	TEXT,
                "description"	TEXT,
                "price"	INTEGER NOT NULL,
                "discount"	INTEGER,
                "homepage"	INTEGER,
                "material"	TEXT,
                "color"	TEXT,
                "size"	TEXT
            );""")

        except:
            pass
        try:
            self.cursor.execute("""CREATE TABLE "stores" (
                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                "name"	TEXT NOT NULL UNIQUE,
                "terms"	BLOB
            );""")
        except:
            pass
        try:
            self.cursor.execute("""CREATE TABLE "users" (
                "name"	TEXT NOT NULL,
                "email"	TEXT NOT NULL UNIQUE,
                "password"	TEXT NOT NULL,
                "type"	TEXT,
                "country"	TEXT,
                "city"	TEXT,
                "street"	TEXT,
                "house_num"	NUMERIC,
                "apartment"	NUMERIC,
                "entrance"	TEXT,
                "zip_code"	NUMERIC,
                "phone"	NUMERIC
            );""")
        except:
            pass
        try:
            self.cursor.execute("""CREATE TABLE "session" (
                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                "email"	TEXT,
                "creation_time"	INTEGER NOT NULL,
                "timestamp"	INTEGER NOT NULL,
                "active"	INTEGER
            );""")
        except:
            pass
        try:
            self.cursor.execute("""CREATE TABLE "orders" (
               CREATE TABLE "orders" (
                "order_number"	NUMERIC NOT NULL,
                "date"	TEXT NOT NULL,
                "email"	TEXT NOT NULL,
                "product"	TEXT NOT NULL,
                "price"	INTEGER NOT NULL
            );""")
        except:
            pass
        if not password:
            password = "password"
        db_filter = {"email": "admin@mail", "password": password, "name": "admin", "type": "admin"}
        self.add_record("users", db_filter)
        self.connection.commit()

if __name__ == "__main__":
    parser = ArgumentParser(description="db_builder")
    parser.add_argument("--db_name", dest="name", help="database name to create")
    parser.add_argument("--password", dest="password", help="initial admin password")
    args = parser.parse_args()
    if not args.name:
        print("must give database name")
        sys.exit(1)
    db = Database(args.name)
    db.connect("new_db")
    db.create_database(args.password)
