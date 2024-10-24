import pytest
from pyscan.drivers.property_settings.dict_property_settings import DictPropertySettings, DictValueException


@pytest.fixture
def settings():
    return DictPropertySettings({
        'name': 'test',
        'dict_values': {
            1: 'one',
            2: 'two',
            'three': 'three',
            'four': 'two',  # Repeated value
            5: 'five',
            'six': 'six',
            7: 'seven',
            'eight': 'six'  # Repeated value
        }
    })


def test_validate_set_value_valid_key(settings):
    assert settings.validate_set_value(1) is True
    assert settings.validate_set_value('three') is True


def test_validate_set_value_invalid_key(settings):
    with pytest.raises(DictValueException):
        settings.validate_set_value('invalid_key')


def test_format_write_value(settings):
    assert settings.format_write_value(1) == 'one'
    assert settings.format_write_value('three') == 'three'


def test_format_query_return(settings):
    assert settings.format_query_return('one') == 1
    assert settings.format_query_return('three') == 'three'


def test_format_query_return_invalid(settings):
    with pytest.raises(KeyError):
        settings.format_query_return('invalid_value')


def test_find_first_key(settings):
    assert settings.find_first_key('one') == 1
    assert settings.find_first_key('three') == 'three'
    assert settings.find_first_key('two') in [2, 'four']  # Adjusted for repeated value
    assert settings.find_first_key('six') in ['six', 'eight']  # Adjusted for repeated value