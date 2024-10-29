# test the set_values_property behavior
import pytest
import typing
from pyscan.general.d_range import drange
from .check_initial_state import check_initial_state


missing_prop_str = "device did not have {} property, test it's in drivers initialize_properties or update_properties."
BAD_INPUTS = [-19812938238312948, -1.11123444859, 3.2222111234, 985767665954, 890992238.2345,
              'not ok', 'bad value',
              [1, 2412, 19], [1, 191, 13, -5.3],
              {'Alfred': "Batman's uncle", 'or': 'imposter'}]
prop_err_str1 = ("attempted to set {} property {} to {} but when queried returned {}."
                 + "\n This is often a sign of interdependent properties that are not suitable for this auto testing."
                 + "test for interdependence and consider blacklisting.")
prop_err_str2 = ("set {} property {} to {} but _{} returned {}."
                 + "\n This is often a sign of interdependent properties that are not suitable for this auto testing."
                 + "test for interdependence and consider blacklisting.")


def test_read_only_property(device, property_name):
    '''
    Tests a read-only property of Range, Values, IndexedValues, or Dict type

    Parameters
    ----------
    device : Subclass of pyscan.drivers.AbstractDriver
        The device to test
    property_name : str
        The name of the property to test
    detailed_dependence : bool
        If True, check if changing this property changes other properties
    initial_state : dict
        key, value pairs of property names and their initial values
    '''

    assert device[property_name], 'Could not read property {}'.format(property_name)


def test_values_property(device, property_name, detailed_dependence, initial_state):
    '''
    Tests a values property

    Parameters
    ----------
    device : Subclass of pyscan.drivers.AbstractDriver
        The device to test
    property_name : str
        The name of the property to test
    detailed_dependence : bool
        If True, check if changing this property changes other properties
    initial_state : dict
        key, value pairs of property names and their initial values
    '''

    settings_name = f'_{property_name}_settings'
    settings = device[settings_name]

    for value in settings.values:
        device[property_name] = value
        assert device[property_name] == value, prop_err_str1.format(
            'values', property_name, str(value) + str(type(value)),
            str(device[property_name]) + str(type(device[property_name])))
        assert device[property_name] == value, prop_err_str2.format(
            'values', property_name, value,
            property_name, property_name)

        if detailed_dependence:
            check_initial_state(device, property_name, initial_state)

    for value in BAD_INPUTS:
        if value not in settings.values:
            with pytest.raises(Exception):
                device[property_name] = value


def decimal_places(x):
    return len(str(x).split('.')[1])


def decimal_floor(x, n):
    val = float('{:.{prec}f}'.format(x, prec=n))
    if val > x:
        return val - 10**(-n)
    else:
        return val


def decimal_ceil(x, n):
    val = float('{:.{prec}f}'.format(x, prec=n))
    if val < x:
        return val + 10**(-n)
    else:
        return val


def test_range_property(device, property_name, detailed_dependence, initial_state):
    '''
    Tests a range property of an instrument

    Parameters
    ----------
    device : Subclass of pyscan.drivers.AbstractDriver
        The device to test
    property_name : str
        The name of the property to test
    detailed_dependence : bool
        If True, check if changing this property changes other properties
    initial_state : dict
        key, value pairs of property names and their initial values
    '''

    settings_name = f'_{property_name}_settings'
    settings = device[settings_name]

    min_range = min(settings.range)
    max_range = max(settings.range)

    with pytest.raises(Exception):
        device[property_name] = min_range - .001
    with pytest.raises(Exception):
        device[property_name] = min_range - 1
    with pytest.raises(Exception):
        device[property_name] = max_range + .001
    with pytest.raises(Exception):
        device[property_name] = max_range + 1

    step = abs(settings.range[1] - settings.range[0]) / 9

    for value in drange(settings.range[0], step, settings.range[1]):

        device[property_name] = value

        new_value = device[property_name]

        n = decimal_places(new_value)

        low = decimal_floor(value, n)
        high = decimal_ceil(value, n)

        assert low <= value <= high, prop_err_str1.format(
            'indexed', property_name, value, device[property_name])


def test_indexed_property(device, property_name, detailed_dependence, initial_state):
    '''
    Tests an indexed property of an instrument

    Parameters
    ----------
    device : Subclass of pyscan.drivers.AbstractDriver
        The device to test
    property_name : str
        The name of the property to test
    detailed_dependence : bool
        If True, check if changing this property changes other properties
    initial_state : dict
        key, value pairs of property names and their initial values
    '''

    settings_name = f'_{property_name}_settings'
    settings = device[settings_name]

    for i, value in enumerate(settings.indexed_values):
        device[property_name] = value

        assert device[property_name] == value, prop_err_str1.format(
            'indexed', property_name, value, device[property_name])
        assert device["_{}".format(property_name)] == value, prop_err_str2.format(
            'indexed', property_name, value, "_{}".format(property_name), device["_{}".format(property_name)])

    for value in BAD_INPUTS:
        if value not in settings.indexed_values:
            with pytest.raises(Exception):
                device[property_name] = value


def test_dict_values_property(device, property_name, detailed_dependence, initial_state):
    '''
    Tests an dict values property of an instrument

    Parameters
    ----------
    device : Subclass of pyscan.drivers.AbstractDriver
        The device to test
    property_name : str
        The name of the property to test
    detailed_dependence : bool
        If True, check if changing this property changes other properties
    initial_state : dict
        key, value pairs of property names and their initial values
    '''

    settings_name = f'_{property_name}_settings'
    settings = device[settings_name]

    for key, value in settings.dict_values.items():
        device[property_name] = value

        err_str1 = ("{} key return not properly formatted. Did not return first key {}, instead returned {}").format(
            property_name, settings.dict_values[key], device[property_name])
        assert device[property_name] == settings.find_first_key(settings.dict_values[key]), err_str1

        err_str2 = ("_{} key return not properly formatted. Did not return first key {}, instead returned {}").format(
            property_name, settings.dict_values[key], device[property_name])
        assert device["_{}".format(property_name)] == settings.find_first_key(settings.dict_values[key]), err_str2

    for bad_input in BAD_INPUTS:
        if isinstance(bad_input, typing.Hashable):
            if bad_input not in settings.dict_values:
                with pytest.raises(Exception):
                    device[property_name] = bad_input
