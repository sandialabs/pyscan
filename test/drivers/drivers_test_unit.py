# -*- coding: utf-8 -*-
import pytest
import math
from collections import OrderedDict
import typing
from test_instrument_driver import TestInstrumentDriver
from pyscan.drivers.test_voltage import TestVoltage

'''
WARNING!
If used without first creating a proper blacklist of _properties that cannot be safely
changed to any value in their range of options based on the driver settings may
cause instruments to self destruct, or lead to significant injury and even DEATH.
ONLY RUN THIS TEST UNIT IF YOU ARE CERTAIN ALL SUCH ATTRIBUTES HAVE BEEN PROPERLY BLACKLISTED!
'''

# not incluing booleans since they can be interpreted ambiguously as ints. Should it?
BAD_INPUTS = [-19812938238312948, -1.11123444859, 3.2222111234, 985767665954, 890992238.2345,
              'not ok', 'bad value', 'Andy is cool',
              [1, 2412, 19], [1, 191, 13, -5.3],
              {'Alfred': "Batman's uncle", 'or': 'imposter'}]


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
    # print(device.__dict__.keys())
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


# check the set_values_property behavior
def check_values_property(device, key):
    name = device[key]['name']

    # reset value to baseline for consistency between tests
    device[name] = device[key]['values'][0]

    for val in BAD_INPUTS:
        if val not in device[key]['values']:
            with pytest.raises(Exception):
                device[name] = val

    for val in device[key]['values']:
        device[name] = val
        # ################ consider within a range here since may not return perfect value.
        assert device["_{}".format(name)] == val
        if not isinstance(device, TestVoltage):
            assert device.query('VALUES?') == str(val)

    # reset value to baseline for consistency between tests
    device[name] = device[key]['values'][0]


# check the set_range_property behavior for a range item
def check_range_property(device, key):
    min_range = min(device[key]['range'])
    max_range = max(device[key]['range'])
    name = device[key]['name']

    # reset range to baseline for consistency between tests
    device[name] = device[key]['range'][0]

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
        assert device['_{}'.format(name)] == r
        # I do not expect this would be ubiquitous and will likely need to be reconsidered for actual drivers.
        if not isinstance(device, TestVoltage):
            assert device.query('RANGE?') == str(r)

    # reset range to baseline for consistency between tests
    device[name] = device[key]['range'][0]


# check the set_range_properties behavior
def check_ranges_property(device, key):
    name = device[key]['name']

    # reset ranges to baseline for consistency between tests
    device[name] = device[key]['ranges'][0]

    ranges = device[key]['ranges']
    num_ranges = len(ranges)
    if num_ranges < 1:
        assert False, "No ranges detected in ranges property"
    min_max_list = []
    for rng in ranges:
        min_range = min(rng)
        max_range = max(rng)
        min_max_list.append((min_range, max_range))

    # iterate over ranges to generate all faulty input combinations with 1 item out of range for each
    bad_entries = []
    for i in range(num_ranges):
        current_min_entry1 = []
        current_min_entry2 = []
        current_max_entry1 = []
        current_max_entry2 = []
        count = 0
        for mn, mx in min_max_list:
            current_min1 = mn
            current_min2 = mn
            current_max1 = mx
            current_max2 = mx
            if i == count:
                current_min1 = mn - .001
                current_min2 = mn - 1
                current_max1 = mx + .001
                current_max2 = mx + 1
            current_min_entry1.append(current_min1)
            current_min_entry2.append(current_min2)
            current_max_entry1.append(current_max1)
            current_max_entry2.append(current_max2)
            count += 1
        bad_entries.append(current_min_entry1)
        bad_entries.append(current_min_entry2)
        bad_entries.append(current_max_entry1)
        bad_entries.append(current_max_entry2)

    # make sure each of those faulty entries fails because they are out of range
    for entry in bad_entries:
        with pytest.raises(Exception):
            device[name] = entry

    # ######### consider updating step size/num steps
    num_steps = []
    for mn, mx in min_max_list:
        current_num_steps = math.floor(abs(mx - mn))
        if current_num_steps > 5:
            current_num_steps = 5
        num_steps.append(current_num_steps)

    # compile a list of good entries that are within the provided ranges
    good_entries = []
    for i in range(num_ranges):
        min_entry = []
        max_entry = []
        for mn, mx in min_max_list:
            min_entry.append(mn)
            max_entry.append(mx)
        good_entries.append(min_entry)
        for j in range(num_steps[i]):
            current_entry_list = []
            count = 0
            for mn, mx in min_max_list:
                current_entry = mn
                if i == count:
                    current_entry = mn + j + 1
                current_entry_list.append(current_entry)
                count += 1
            good_entries.append(current_entry_list)
        good_entries.append(max_entry)

    # make sure each of the good entries succeeds
    for entry in good_entries:
        device[name] = entry
        assert device._ranges == entry
        if not isinstance(device, TestVoltage):
            assert device.query('RANGES?') == str(entry)

    # reset ranges to baseline for consistency between tests
    device[name] = device[key]['ranges'][0]


# check the set_indexed_values_property behavior
def check_indexed_property(device, key):
    # check a random string rather than a for loop
    name = device[key]['name']

    # reset value to baseline for consistency between tests
    device[name] = device[key]['indexed_values'][0]

    for item in BAD_INPUTS:
        if item not in device[key]['indexed_values']:
            with pytest.raises(Exception):
                device[name] = item

    for idx, iv in enumerate(device[key]['indexed_values']):
        # print(str(iv), str(idx), name, device[name])
        device[name] = iv
        assert device["_{}".format(name)] == iv
        # print("underscore property is: ", device["_{}".format(name)])
        if not isinstance(device, TestVoltage):
            query_string = device[key]['query_string']
            err_string = ("query returns: {} is not the idx: {} for: {}"
                          .format(device.query(query_string), str(idx), key))
            assert device.query(query_string).strip("\n") == str(idx), err_string

    # reset value to baseline for consistency between tests
    device[name] = device[key]['indexed_values'][0]


# check the set_dict_values_property behavior
def check_dict_property(device, key):
    # key must be string or number, set property to include lists, arrays, arbritray values of diversity
    name = device[key]['name']
    ord_dict = OrderedDict(device[key]['dict_values'])

    # reset the dict value to the first value for consistency between tests
    for k in ord_dict:
        device[name] = k
        break

    for k in device[key]['dict_values']:
        # print(k)
        device[name] = k
        assert device["_{}".format(name)] == device.find_first_key(ord_dict, ord_dict[k])
        if not isinstance(device, TestVoltage):
            query_string = device[key]['query_string']
            # print(key, device[key]['dict_values'][k], device.query(query_string))
            assert device.query(query_string).strip('\n') == str(device[key]['dict_values'][k])

    for item in BAD_INPUTS:
        if isinstance(item, typing.Hashable):
            if item not in device[key]['dict_values']:
                with pytest.raises(Exception):
                    device[name] = item

    # reset the dict value to the first value for consistency between tests
    for k in ord_dict:
        device[name] = k
        break


# implements above checks for all attributes by type
def check_properties(test_instrument):
    # This is a critical step to ensuring safety when testing drivers with actual instruments
    validate_blacklist(test_instrument)

    # iterate over all attributes to test accordingly using predefined functions
    values_counter, range_counter, ranges_counter, idx_vals_counter, dict_vals_counter = 0, 0, 0, 0, 0
    instrument_name = test_instrument.__class__.__name__
    # values_idx, range_idx, ranges_idx, idx_vals_idx, dict_vals_idx = [], [], [], [], []
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
        if hasattr(test_instrument, 'black_list_for_testing'):
            base_name = name.replace('_settings', '')
            # base_name = test_instrument[name]['name']
            if base_name in test_instrument['black_list_for_testing']:
                continue
        keys = test_instrument[name].keys()
        if ('values' in keys) and ('indexed_' not in keys) and ('dict_' not in keys):
            values_counter += 1
            # values_idx.append(values_counter)
            check_values_property(test_instrument, name)
        elif 'range' in keys and ('ranges' not in keys):
            range_counter += 1
            # range_idx.append(range_counter)
            check_range_property(test_instrument, name)
        elif 'ranges' in keys:
            ranges_counter += 1
            # ranges_idx.append(range_counter)
            check_ranges_property(test_instrument, name)
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
                name, ['values', 'range', 'ranges', 'indexed_values', 'dict_values'])

    restored_settings = restore_initial_state(test_instrument, saved_settings)

    diff = set(restored_settings) ^ set(saved_settings)

    mid_string = 'properties found and tested out of'
    print("{} range {} {} total settings found.".format(range_counter, mid_string, total_settings))
    print("{} ranges {} {} total settings found.".format(ranges_counter, mid_string, total_settings))
    print("{} values {} {} total settings found.".format(values_counter, mid_string, total_settings))
    print("{} indexed values {} {} total settings found.".format(idx_vals_counter, mid_string, total_settings))
    print("{} dict values {} {} total settings found.".format(dict_vals_counter, mid_string, total_settings))
    try:
        print("{} blacklisted settings not testing (likely due to interdependencies not suitable for automated testing)"
              .format(len(test_instrument.black_list_for_testing)))
    except Exception:
        pass
    total_tested = range_counter + ranges_counter + values_counter + idx_vals_counter + dict_vals_counter
    print("{} properties tested out of {} total settings.".format(total_tested, total_settings))

    if isinstance(test_instrument, TestInstrumentDriver):
        assert values_counter == range_counter == ranges_counter == idx_vals_counter == dict_vals_counter == 1
        print("Drivers test unit seems to be working as expected.")
    print("Settings restored to: {}".format(restored_settings))
    if (len(diff) > 0):
        print("Restored settings are different for the following: ", diff)


def test_driver(device=TestInstrumentDriver(), expected_attributes=None, expected_values=None):
    if expected_attributes is not None:
        check_has_attributes(device, expected_attributes)

        if expected_values is not None:
            check_attribute_values(device, expected_attributes, expected_values)

    check_properties(device)

    print("Tests passed, instrument {} should be ready to go.".format(device.__class__.__name__))
