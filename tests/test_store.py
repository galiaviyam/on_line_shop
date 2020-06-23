from store import Store
from user import User
from database import Database
import json
from mock import patch, mock_open
import os


def prepare_store(mocker):
    with open("test_config.json", "w") as f:
        f.write('{ "store_name": "Goldilocks", "database_name": "Goldilocks.db",  "timeout": 3600}')
    mocker.patch.object(Database, 'get_record')
    mocker.patch.object(Database, 'get_records')
    mocker.patch.object(User, "check_session")
    User.check_session.return_value = True
    Database.get_records.return_value = {}
    store = Store("test_config.json")
    store.get_store()
    return store


def test_get_store_empty_list(mocker):
    with open("test_config.json", "w") as f:
        f.write('{ "store_name": "Goldilocks", "database_name": "Goldilocks.db",  "timeout": 3600}')
    mocker.patch.object(Database, 'get_record')
    mocker.patch.object(Database, 'get_records')
    mocker.patch.object(User, "check_session")
    User.check_session.return_value = True
    mocker.patch.object(Store, 'get_categories')
    #Database.get_records.return_value = {"1": {"sku": "1001", "name": "", "price": 123}}
    Database.get_records.return_value = {}
    Database.get_record.return_value = {"name": "", "terms": ""}
    mocker.patch.object(json, 'load')
    store = Store("test_config.json")
    mocker.patch.object(Store, 'get_categories')
    store.get_store()
    assert [] == store.product_list
    os.remove("test_config.json")


def test_get_store_one_item(mocker):
    with open("test_config.json", "w") as f:
        f.write('{ "store_name": "MyShop", "database_name": "MyShop.db",  "timeout": 3600}')
    mocker.patch.object(Database, 'get_record')
    mocker.patch.object(Database, 'get_records')
    mocker.patch.object(User, "check_session")
    User.check_session.return_value = True
    mocker.patch.object(Store, 'get_categories')
    Database.get_records.return_value = {"1": {"sku": "1001",
                                               "name": "",
                                               "price": "",
                                               "discount": "",
                                               "final_price": "",
                                               "description": "",
                                               "material": "",
                                               "color": "",
                                               "size": 123
                                            }}
    Database.get_record.return_value = {"name": "", "terms": ""}
    mocker.patch.object(json, 'load')
    store = Store("test_config.json")
    mocker.patch.object(Store, 'get_categories')
    store.get_store()
    assert 1 == len(store.product_list)
    os.remove("test_config.json")


def test_get_categories(mocker):
    store = prepare_store(mocker)
    Database.get_records.return_value = {"1": {"category": "rings"}, "2": {"category": "necklaces"}}
    store.get_categories()
    assert store.categories == {"rings": "1", "necklaces": "2"}
    os.remove("test_config.json")


def test_get_users(mocker):
    store = prepare_store(mocker)
    Database.get_records.return_value = {"1": {"email": "test", "type": "client"}, "2": {"email": "testy", "type": "seller"}}
    result = store.get_users("client")
    assert result == {"1": {"email": "test", "type": "client"}, "2": {"email": "testy", "type": "seller"}}
    os.remove("test_config.json")


def test_search(mocker):
    store = prepare_store(mocker)
    mocker.patch.object(Database, 'search')
    Database.search.return_value = {"1": { "sku": "1001",
                                           "name": "ring",
                                           "price": "",
                                           "discount": "",
                                           "final_price": "",
                                           "description": "",
                                           "material": "",
                                           "color": "",
                                           "size": 123
                                            }}
    result = store.search("ring")
    assert 1 == len(result)
    os.remove("test_config.json")


def test_get_by_category(mocker):
    store = prepare_store(mocker)
    Database.get_records.return_value = {"1": {"sku": "1001",
                                               "name": "ring",
                                               "price": "",
                                               "discount": "",
                                               "final_price": "",
                                               "description": "",
                                               "material": "",
                                               "color": "",
                                               "size": 123
                                            }}
    result = store.get_by_category("rings")
    assert 1 == len(result)
    result = store.get_by_category("")
    assert 1 == len(result)
    os.remove("test_config.json")


def test_add_user(mocker):
    store = prepare_store(mocker)


def test_delete_user(mocker):
    store = prepare_store(mocker)


def test_get_product_price(mocker):
    store = prepare_store(mocker)


def test_add_product(mocker):
    store = prepare_store(mocker)