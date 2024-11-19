import pyscan as ps
import pytest


@pytest.fixture
def ia():
    ia = ps.ItemAttribute()
    ia.test_prop1 = 3
    ia.test_prop2 = 'str'
    return ia


def test_itemattribute_property_call(ia):
    assert ia.test_prop1 == 3
    assert ia.test_prop2 == 'str'


@pytest.mark.parametrize("key,value", [
    ('test_prop1', 3),
    ('test_prop2', 'str')])
def test_itemattribute_dict_call(ia, key, value):
    assert ia[key] == value


@pytest.mark.parametrize("func,value", [
    ('keys', ['test_prop1', 'test_prop2']),
    ('values', [3, 'str']),
    ('items', [('test_prop1', 3), ('test_prop2', 'str')])])
def test_itemattribute_dictionary_functions(ia, func, value):
    assert list(getattr(ia, func)()) == value


@pytest.mark.parametrize("key", [
    'test_prop1',
    'test_prop2'])
def test_itemattribute_del(ia, key):
    del ia[key]
    assert not hasattr(ia, key)


@pytest.mark.parametrize("key", [
    'test_prop1',
    'test_prop2'])
def test_itemattribute_contains(ia, key):
    assert key in ia
