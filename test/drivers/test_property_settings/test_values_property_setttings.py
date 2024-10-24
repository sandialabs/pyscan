import pytest
from pyscan.drivers.property_settings.values_property_settings import ValuesPropertySettings, ValueException

@pytest.fixture
def settings():
    return ValuesPropertySettings({'name': 'test', 'values_list': [1, 2, 3, 'a', 'b', 'c']})


def test_validate_set_value_valid(settings):
    assert settings.validate_set_value(1) is True
    assert settings.validate_set_value('a') is True


def test_validate_set_value_invalid(settings):
    with pytest.raises(ValueException):
        settings.validate_set_value(4)
    with pytest.raises(ValueException):
        settings.validate_set_value('d')


def test_format_write_value(settings):
    assert settings.format_write_value(1) == 1
    assert settings.format_write_value('a') == 'a'


def test_format_query_return_valid(settings):
    assert settings.format_query_return('1') == 1
    assert settings.format_query_return('a') == 'a'


def test_format_query_return_invalid(settings):
    with pytest.raises(ValueError):
        settings.format_query_return('d')