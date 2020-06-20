from store import Store
from database import Database
import json
from mock import patch, mock_open


def test_get_categories(mocker):
    mocker.patch.object(Database, 'get_records')
    Database.get_records.return_value = {"1": {"category": "rings"}, "2": {"category": "necklaces"}}
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

@patch("database.Database")
def test_get_store(mocker):
    mocker.patch.object(Database, 'connect')
    mocker.patch.object(Database, 'get_record')
    mocker.patch.object(Database, 'get_records')
    Database.get_records.return_value = {"1": {"sku": "1001", "name": "", "price": 123}}
    Database.get_record.return_value = {"name": "", "terms": ""}
    with patch("builtins.open", mock_open(read_data="data")) as file:
        mocker.patch.object(json, 'load')
        store = Store("my_shop")
        mocker.patch.object(Store, 'get_categories')
        store.get_store()
        assert {} == store.product_list

def search(mocker):
    assert False

def get_by_category(mocker):
    assert False

def show_cart(mocker):
    assert False

def show_wishlist(mocker):
    assert False