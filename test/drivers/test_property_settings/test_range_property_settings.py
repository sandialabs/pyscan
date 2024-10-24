import pytest
from pyscan.drivers.property_settings.range_property_settings import RangePropertySettings, RangeException


@pytest.fixture
def settings():
    return RangePropertySettings({'name': 'test', 'range': (0, 10)})


def test_validate_set_value_within_range(settings):
    assert settings.validate_set_value(5) is True


def test_validate_set_value_below_range(settings):
    with pytest.raises(RangeException):
        settings.validate_set_value(-1)


def test_validate_set_value_above_range(settings):
    with pytest.raises(RangeException):
        settings.validate_set_value(11)


def test_format_write_value(settings):
    assert settings.format_write_value(5) == 5


def test_format_query_return(settings):
    assert settings.format_query_return('5.5') == 5.5


def test_validate_set_value_edge_case_lower(settings):
    assert settings.validate_set_value(0) is True


def test_validate_set_value_edge_case_upper(settings):
    assert settings.validate_set_value(10) is True


def test_format_query_return_integer(settings):
    assert settings.format_query_return('5') == 5.0


def test_format_query_return_invalid(settings):
    with pytest.raises(ValueError):
        settings.format_query_return('invalid')
