# -*- coding: utf-8 -*-
import pytest
import math
from collections import OrderedDict
import typing
from test_instrument_driver import TestInstrumentDriver
from pyscan.drivers.test_voltage import TestVoltage


# not incluing booleans since they can be interpreted ambiguously as ints. Should it?
BAD_INPUTS = [-19812938238312948, -1.11123444859, 3.2222111234, 985767665954, 890992238.2345,
              'not ok', 'bad value', 'Andy is cool',
              [1, 2412, 19], [1, 191, 13, -5.3],
              {'Alfred': "Batman's uncle", 'or': 'imposter'}]


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


# check the set_range_property behavior for a range item
def check_range_property(device, key):
    min_range = min(device[key]['range'])
    max_range = max(device[key]['range'])
    name = device[key]['name']
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

    for r in range(device[key]['range'][0], device[key]['range'][0], step):
        device[name] = r
        assert device['_{}'.format(name)] == r
        # I do not expect this would be ubiquitous and will likely need to be reconsidered for actual drivers.
        if not isinstance(device, TestVoltage):
            assert device.query('RANGE?') == str(r)


# check the set_range_properties behavior
def check_ranges_property(device, key):
    name = device[key]['name']
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


# check the set_indexed_values_property behavior
def check_indexed_property(device, key):
    # check a random string rather than a for loop
    name = device[key]['name']

    for item in BAD_INPUTS:
        if item not in device[key]['indexed_values']:
            with pytest.raises(Exception):
                device[name] = item

    for iv in device._indexed_values_settings['indexed_values']:
        device[name] = iv
        assert device["_{}".format(name)] == iv
        if not isinstance(device, TestVoltage):
            assert device.query('INDEXED_VALUES?') == str(iv)


# check the set_dict_values_property behavior
def check_dict_property(device, key):
    # key must be string or number, set property to include lists, arrays, arbritray values of diversity
    name = device[key]['name']
    ord_dict = OrderedDict(device[key]['dict_values'])
    for k in device[key]['dict_values']:
        device[name] = k
        assert device["_{}".format(name)] == device.find_first_key(ord_dict, ord_dict[k])
        if not isinstance(device, TestVoltage):
            assert device.query('DICT_VALUES?') == device.find_first_key(ord_dict, ord_dict[k])

    for item in BAD_INPUTS:
        if isinstance(item, typing.Hashable):
            if item not in device[key]['dict_values']:
                with pytest.raises(Exception):
                    device[name] = item


# implements above checks for all attributes by type
def check_properties(test_instrument):
    # iterate over all attributes to test accordingly using predefined functions
    values_counter, range_counter, ranges_counter, idx_vals_counter, dict_vals_counter = 0, 0, 0, 0, 0
    # values_idx, range_idx, ranges_idx, idx_vals_idx, dict_vals_idx = [], [], [], [], []
    print("Beginning tests for: ", test_instrument.__class__.__name__)
    settings = []
    total_settings = 0
    for attribute_name in test_instrument.__dict__.keys():
        if "_settings" in attribute_name:
            settings.append(attribute_name)
            total_settings += 1

    for name in settings:
        if 'values' in test_instrument[name].keys():
            values_counter += 1
            # values_idx.append(values_counter)
            check_values_property(test_instrument, name)
        elif 'range' in test_instrument[name].keys():
            range_counter += 1
            # range_idx.append(range_counter)
            check_range_property(test_instrument, name)
        elif 'ranges' in test_instrument[name].keys():
            ranges_counter += 1
            # ranges_idx.append(range_counter)
            check_ranges_property(test_instrument, name)
        elif 'indexed_values' in test_instrument[name].keys():
            idx_vals_counter += 1
            # idx_vals_idx.append(idx_vals_counter)
            check_indexed_property(test_instrument, name)
        elif 'dict_values' in test_instrument[name].keys():
            dict_vals_counter += 1
            # dict_vals_idx.append(dict_vals_counter)
            check_dict_property(test_instrument, name)
        else:
            assert False, "no valid type present in setting: {}. Must be one of {}.".format(
                name, ['values', 'range', 'ranges', 'indexed_values', 'dict_values'])

    mid_string = 'properties found and tested out of'
    print("{} range {} {} total settings found.".format(range_counter, mid_string, total_settings))
    print("{} ranges {} {} total settings found.".format(ranges_counter, mid_string, total_settings))
    print("{} values {} {} total settings found.".format(values_counter, mid_string, total_settings))
    print("{} indexed values {} {} total settings found.".format(idx_vals_counter, mid_string, total_settings))
    print("{} dict values {} {} total settings found.".format(dict_vals_counter, mid_string, total_settings))

    if isinstance(test_instrument, TestInstrumentDriver):
        assert values_counter == range_counter == ranges_counter == idx_vals_counter == dict_vals_counter == 1
        print("Drivers test unit seems to be working as expected.")


def test_driver(device=TestInstrumentDriver(), expected_attributes=None, expected_values=None):
    if expected_attributes is not None:
        check_has_attributes(device, expected_attributes)

        if expected_values is not None:
            check_attribute_values(device, expected_attributes, expected_values)

    check_properties(device)

    print("Tests passed, instrument {} should be ready to go.".format(device.__class__.__name__))
