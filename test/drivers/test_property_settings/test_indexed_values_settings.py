import pytest
from pyscan.drivers.property_settings.indexed_property_settings import IndexedPropertySettings, IndexedValueException


@pytest.fixture
def settings():
    return IndexedPropertySettings({
        'name': 'test',
        'indexed_values': [0, 1, 2, 3, 4, 'a', 'b', 'c', 'd', True, False]})


def test_validate_set_value_within_index(settings):
    assert settings.validate_set_value(2) is True


def test_validate_set_value_below_index(settings):
    with pytest.raises(IndexedValueException):
        settings.validate_set_value(-1)


def test_validate_set_value_above_index(settings):
    with pytest.raises(IndexedValueException):
        settings.validate_set_value(5)


def test_format_write_value(settings):
    assert settings.format_write_value(3) == 3


def test_format_query_return(settings):
    assert settings.format_query_return('2') == 2


def test_validate_set_value_edge_case_lower(settings):
    assert settings.validate_set_value(0) is True


def test_validate_set_value_edge_case_upper(settings):
    assert settings.validate_set_value(4) is True


def test_format_query_return_invalid(settings):
    with pytest.raises(ValueError):
        settings.format_query_return('invalid')
