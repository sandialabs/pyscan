# -*- coding: utf-8 -*-
import pytest
import math
from collections import OrderedDict
import typing
from pyscan.drivers.testing.test_instrument_driver import TestInstrumentDriver
from pyscan.general.get_version import get_driver_version

'''
WARNING!
If used without first creating a proper blacklist of _properties that cannot be safely
changed to any value in their range of options based on the driver settings may
cause instruments to self destruct, or lead to significant injury and even DEATH.
Depending on the instrument and how it's set up this may or may not be a relevant issue.
If there are any settings that could be changed to risk harming some or the instrument
blacklist them before proceeding by adding a self.black_list_for_testing property at the end
of the instrument driver's __init__.
ONLY RUN THIS TEST UNIT IF YOU ARE CERTAIN ALL SUCH ATTRIBUTES HAVE BEEN PROPERLY BLACKLISTED!
'''

# not incluing booleans since they can be interpreted ambiguously as ints. Should it?
BAD_INPUTS = [-19812938238312948, -1.11123444859, 3.2222111234, 985767665954, 890992238.2345,
              'not ok', 'bad value', 'Andy is cool',
              [1, 2412, 19], [1, 191, 13, -5.3],
              {'Alfred': "Batman's uncle", 'or': 'imposter'}]


missing_prop_str = "device did not have {} property, check it's in drivers initialize_properties or update_properties."
prop_err_str1 = ("attempted to set {} property {} to {} but when queried returned {}."
                 + "\n This is often a sign of interdependent properties that are not suitable for this auto testing."
                 + "Check for interdependence and consider blacklisting.")
prop_err_str2 = ("set {} property {} to {} but _{} returned {}."
                 + "\n This is often a sign of interdependent properties that are not suitable for this auto testing."
                 + "Check for interdependence and consider blacklisting.")


# This function is critical step to ensuring safety when testing drivers with actual instruments
def validate_blacklist(test_instrument):
    settings = []
    settings_names = []
    total_settings = 0
    for attribute_name in test_instrument.__dict__.keys():
        if "_settings" in attribute_name:
            settings.append(attribute_name)
            _name = "_{}".format(test_instrument[attribute_name]['name'])
            settings_names.append(_name)
            total_settings += 1

    if hasattr(test_instrument, 'black_list_for_testing'):
        for blacklisted in test_instrument.black_list_for_testing:
            err_msg = "WARNING, blacklisted attribute could not be validated and does not match a driver property"
            assert blacklisted in settings_names, err_msg
            count = 0
            for i in test_instrument.black_list_for_testing:
                if i == blacklisted:
                    count += 1
            if count > 1:
                assert False, "There appear to be duplicates in your blacklist."
    else:
        err_msg = str("Warning, driver needs black_list_for_testing attribute, please double check if there are \n"
                      + "any attributes that need to be blacklisted for safety purposes, as non-blacklisted settings \n"
                      + "will be iterated through the entirety of their range and could cause significant injury or \n"
                      + "even death to nearby users and permanently damage instruments if used improperly. \n"
                      + "If no properties are to be blacklisted for testing, please set the black_list_for_testing \n"
                      "attribute to an empty list as acknowledgment of this warning to continue.")
        assert False, err_msg


def save_initial_state(device):
    saved_settings = []
    print(device.__dict__.keys())
    for attribute_name in device.__dict__.keys():
        if "_settings" in attribute_name:
            '''try:
                name = "_{}".format(device[attribute_name]['name'])
                val = device[name]
            except (Exception):'''
            name = "{}".format(device[attribute_name]['name'])
            val = device[name]
            if 'ranges' in device[attribute_name].keys():
                val = tuple(val)
            saved_settings.append((name, val))
            # print(device.__dict__.keys())

    return saved_settings


def restore_initial_state(device, saved_settings):
    restored_settings = []
    for setting in saved_settings:
        setter = setting[0]
        _name = "_{}".format(setter)
        val = setting[1]

        if _name in device.black_list_for_testing:
            err_msg = ("WARNING! BLACKLISTED PROPERTY WAS SOMEHOW CHANGED. Was {}, now {}\n".format(val, device[setter])
                       + "PROCEED WITH CAUTION!")
            assert val == device[setter], err_msg
            restored_settings.append((setter, device[setter]))
            continue

        if 'ranges' in device["_{}_settings".format(setter)].keys():
            val = device["_{}_settings".format(setter)]['return_type'](val)
        try:
            device[setter] = val
        except Exception:
            try:
                device[setter] = device["_{}_settings".format(setter)]['return_type'](val)
            except Exception:
                assert False, ("setter is: {} saved setting is: {} val is: {}"
                               .format(setter, setting, val))
        query_result = device[setter]
        if 'ranges' in device["_{}_settings".format(setter)].keys():
            query_result = tuple(query_result)
        restored_settings.append((setter, query_result))

    return restored_settings


def reset_device_properties(device):
    settings = []
    for attribute_name in device.__dict__.keys():
        if "_settings" in attribute_name:
            settings.append(attribute_name)

    blacklisted = []
    for name in settings:
        keys = device[name].keys()
        var_name = name.replace('_settings', '')
        if var_name in device.black_list_for_testing:
            blacklisted.append((var_name, device[var_name]))
            continue
        if ('values' in keys) and ('indexed_' not in keys) and ('dict_' not in keys):
            device[var_name] = device[name]['values'][0]
        elif 'range' in device[name].keys():
            device[var_name] = device[name]['range'][0]
        elif 'ranges' in device[name].keys():
            # write to reset val later
            pass
        elif 'indexed_values' in device[name].keys():
            device[var_name] = device[name]['indexed_values'][0]
        elif 'dict_values' in device[name].keys():
            for key in device[name]['dict_values'].keys():
                device[var_name] = key
                break
        else:
            assert False, "no valid type present in setting: {}. Must be one of {}.".format(
                name, ['values', 'range', 'ranges', 'indexed_values', 'dict_values'])

    if len(blacklisted) > 0:
        print("These blacklisted settings and their corresponding values were not reset: ", blacklisted)


# check that the initialized state has the expected attributes
def check_has_attributes(device, attributes):
    for a in attributes:
        assert hasattr(device, a), "test device does not have {} attribute when initialized".format(a)


# check that the initialized attributes have the expected values
def check_attribute_values(device, attributes, ev):
    for i in range(len(ev)):
        err_string = "test device {} attribute does not equal {}".format(device[attributes[i]], ev[i])
        assert (device[attributes[i]] == ev[i]), err_string


# designed for testing read only properties of any type
def check_read_only_property(device, key):
    name = device[key]['name']
    settings = device[name + '_settings']
    return_type = device

    # I'm not sure that this will work. It might be that only the underscore property can be used to access
    # the property value.
    assert type(device[name]) is return_type, "read_only property {} returned type {} not {}".format(
        name, type(device[name]), return_type)
    assert type(device["_{}".format(name)]) is return_type, "read_only _property {} returned type {} not {}".format(
        name, type(device["_{}".format(name)]), return_type)

    assert 'write_string' not in settings, "read_only property {} has write_string {}".format(
        name, settings['write_string'])

    # I'm not sure that this will fail. If not, it should be that the original value remains the same no matter what
    # you try to set it to.
    for val in BAD_INPUTS:
        with pytest.raises(Exception):
            device[name] = val


# check the set_values_property behavior
def check_values_property(device, key):
    name = device[key]['name']

    # reset value to baseline for consistency between tests
    try:
        device[name] = device[key]['values'][0]
    except Exception:
        assert False, missing_prop_str.format(name)

    for val in BAD_INPUTS:
        if val not in device[key]['values']:
            with pytest.raises(Exception):
                device[name] = val

    for val in device[key]['values']:
        device[name] = val
        # ################ consider within a range here since may not return perfect value.
        assert device[name] == val, prop_err_str1.format('values', name, val, device[name])
        assert device["_{}".format(name)] == val, prop_err_str2.format('values', name, val,
                                                                       "_{}".format(name), device["_{}".format(name)])

    # reset value to baseline for consistency between tests
    device[name] = device[key]['values'][0]


# check the set_range_property behavior for a range item
def check_range_property(device, key):
    min_range = min(device[key]['range'])
    max_range = max(device[key]['range'])
    name = device[key]['name']

    # reset range to baseline for consistency between tests
    try:
        device[name] = device[key]['range'][0]
    except Exception:
        assert False, missing_prop_str.format(name)

    with pytest.raises(Exception):
        device[name] = min_range - .001
    with pytest.raises(Exception):
        device[name] = min_range - 1
    with pytest.raises(Exception):
        device[name] = max_range + .001
    with pytest.raises(Exception):
        device[name] = max_range + 1

    # set fixed number of steps to divide the overall range by for step size for actual drivers
    # ################# change these number of steps to follow ranges.
    step = 1
    if abs(device[key]['range'][0] - device[key]['range'][0]) > 10000:
        step = math.ceil(abs(device[key]['range'][0] - device[key]['range'][0]) / 1000)

    for r in range(int(device[key]['range'][0]), int(device[key]['range'][0]), step):
        device[name] = r
        assert device[name] == r, prop_err_str1.format('range', name, r, device[name])
        assert device['_{}'.format(name)] == r, prop_err_str2.format('range', name, r,
                                                                     "_{}".format(name), device["_{}".format(name)])

    # reset range to baseline for consistency between tests
    device[name] = device[key]['range'][0]


# check the set_indexed_values_property behavior
def check_indexed_property(device, key):
    # check a random string rather than a for loop
    name = device[key]['name']

    # reset value to baseline for consistency between tests
    try:
        device[name] = device[key]['indexed_values'][0]
    except Exception:
        assert False, missing_prop_str.format(name)

    for item in BAD_INPUTS:
        if item not in device[key]['indexed_values']:
            with pytest.raises(Exception):
                device[name] = item

    for idx, iv in enumerate(device[key]['indexed_values']):
        # print(str(iv), str(idx), name, device[name])
        device[name] = iv
        assert device[name] == iv, prop_err_str1.format('indexed', name, iv, device[name])
        assert device["_{}".format(name)] == iv, prop_err_str2.format('indexed', name, iv,
                                                                      "_{}".format(name), device["_{}".format(name)])
        # print("underscore property is: ", device["_{}".format(name)])

    # reset value to baseline for consistency between tests
    device[name] = device[key]['indexed_values'][0]


# check the set_dict_values_property behavior
def check_dict_property(device, key):
    # key must be string or number, set property to include lists, arrays, arbritray values of diversity
    name = device[key]['name']
    ord_dict = OrderedDict(device[key]['dict_values'])

    # reset the dict value to the first value for consistency between tests
    for k in ord_dict:
        try:
            device[name] = k
        except Exception:
            assert False, missing_prop_str.format(name)
        break

    for k in device[key]['dict_values']:
        # print(k)
        device[name] = k
        err_str1 = ("{} key return not properly formatted. Did not return first key {}, instead returned {}").format(
            name, device.find_first_key(ord_dict, ord_dict[k]), device[name])
        assert device[name] == device.find_first_key(ord_dict, ord_dict[k]), err_str1
        err_str2 = ("_{} key return not properly formatted. Did not return first key {}, instead returned {}").format(
            name, device.find_first_key(ord_dict, ord_dict[k]), device[name])
        assert device["_{}".format(name)] == device.find_first_key(ord_dict, ord_dict[k]), err_str2

    for bad_input in BAD_INPUTS:
        if isinstance(bad_input, typing.Hashable):
            if bad_input not in device[key]['dict_values']:
                with pytest.raises(Exception):
                    device[name] = bad_input

    # reset the dict value to the first value for consistency between tests
    for k in ord_dict:
        device[name] = k
        break


# implements above checks for all attributes by type
def check_properties(test_instrument):
    # This is a critical step to ensuring safety when testing drivers with actual instruments
    validate_blacklist(test_instrument)

    # iterate over all attributes to test accordingly using predefined functions
    values_counter, range_counter, idx_vals_counter, dict_vals_counter = 0, 0, 0, 0
    instrument_name = test_instrument.__class__.__name__
    # values_idx, range_idx, idx_vals_idx, dict_vals_idx = [], [], [], []
    saved_settings = save_initial_state(test_instrument)
    print("Initial state for the {} was: {}".format(instrument_name, saved_settings))

    reset_device_properties(test_instrument)
    reset_settings = save_initial_state(test_instrument)
    print("Reset state for the {} was: {}".format(instrument_name, reset_settings))

    print("Beginning tests for: ", test_instrument.__class__.__name__)

    settings = []
    total_settings = 0
    for attribute_name in test_instrument.__dict__.keys():
        if "_settings" in attribute_name:
            settings.append(attribute_name)
            total_settings += 1

    for name in settings:
        # if hasattr(test_instrument, 'black_list_for_testing'):
        base_name = name.replace('_settings', '')
        # base_name = test_instrument[name]['name']
        if base_name in test_instrument['black_list_for_testing']:
            continue
        keys = test_instrument[name].keys()
        if 'read_only' in keys:
            check_read_only_property(test_instrument, name)
        elif ('values' in keys) and ('indexed_' not in keys) and ('dict_' not in keys):
            values_counter += 1
            # values_idx.append(values_counter)
            check_values_property(test_instrument, name)
        elif 'range' in keys:
            range_counter += 1
            # range_idx.append(range_counter)
            check_range_property(test_instrument, name)
        elif 'indexed_values' in keys:
            idx_vals_counter += 1
            # idx_vals_idx.append(idx_vals_counter)
            check_indexed_property(test_instrument, name)
        elif 'dict_values' in keys:
            dict_vals_counter += 1
            # dict_vals_idx.append(dict_vals_counter)
            check_dict_property(test_instrument, name)
        else:
            assert False, "no valid type present in setting: {}. Must be one of {}.".format(
                name, ['values', 'range', 'indexed_values', 'dict_values'])

    restored_settings = restore_initial_state(test_instrument, saved_settings)

    diff = set(restored_settings) ^ set(saved_settings)

    mid_string = 'properties found and tested out of'
    print("{} range {} {} total settings found.".format(range_counter, mid_string, total_settings))
    print("{} values {} {} total settings found.".format(values_counter, mid_string, total_settings))
    print("{} indexed values {} {} total settings found.".format(idx_vals_counter, mid_string, total_settings))
    print("{} dict values {} {} total settings found.".format(dict_vals_counter, mid_string, total_settings))
    try:
        print("{} blacklisted settings not testing (likely due to interdependencies not suitable for automated testing)"
              .format(len(test_instrument.black_list_for_testing)))
    except Exception:
        pass
    total_tested = range_counter + values_counter + idx_vals_counter + dict_vals_counter
    print("{} properties tested out of {} total settings.".format(total_tested, total_settings))

    if isinstance(test_instrument, TestInstrumentDriver):
        assert values_counter == range_counter == idx_vals_counter == dict_vals_counter == 1
        print("Drivers test unit seems to be working as expected.")
    print("Settings restored to: {}".format(restored_settings))
    if (len(diff) > 0):
        print("Restored settings are different for the following: ", diff)


def test_driver(device=TestInstrumentDriver(), iterate_version=True, expected_attributes=None, expected_values=None):
    if expected_attributes is not None:
        check_has_attributes(device, expected_attributes)

        if expected_values is not None:
            check_attribute_values(device, expected_attributes, expected_values)

    check_properties(device)

    print("Tests passed, instrument {} should be ready to go.".format(device.__class__.__name__))
    if iterate_version is True:
        try:
            instrument_id = self.instrument.query('*IDN?')
            

