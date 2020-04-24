import sys, os

sys.path.append(os.path.dirname( os.path.abspath(__file__)))
from store import Store
from database import Database
from mock import patch

def test_get_categories(mocker):
    mocker.patch.object(Database, 'get_records')
    Database.get_records.return_value = {"1": "rings", "2": "necklaces"}
    store = Store("my_shop")
    store.db = Database("db_test")
    store.get_categories()
    assert store.categories == {"rings": "1", "necklaces": "2"}

def test_get_categories_empty_table(mocker):
    mocker.patch.object(Database, 'get_records')
    Database.get_records.return_value = {}
    store = Store("my_shop")
    store.db = Database("db_test")
    store.get_categories()
    assert store.categories == {}
