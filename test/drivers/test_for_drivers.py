# -*- coding: utf-8 -*-
import pytest
import math
import string
from collections import OrderedDict

# not incluing booleans since they can be interpreted ambiguously as ints. Should it?
BAD_INPUTS = [-19812938238312948, -1.11123444859, 3.2222111234, 985767665954, 890992238.2345,
                  'not ok', 'bad value', 'Andy is cool',
                  [1, 2412, 19], [1, 191, 13, -5.3],
                  {'Alfred': "Batman's uncle", 'or': 'imposter'},
                  {'key1': 'bad boy', 'key2': 'badder girl'}]


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
        assert device["_{}".format(name)] == val
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
    step = 1
    if abs(device[key]['range'][0] - device[key]['range'][0]) > 10000:
        step = math.ceil(abs(device[key]['range'][0] - device[key]['range'][0]) / 1000)

    for r in range(device[key]['range'][0], device[key]['range'][0], step):
        device[name] = r
        assert device['_{}'.format(name)] == r
        # I do not expect this would be ubiquitous and will likely need to be reconsidered for actual drivers.
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
        assert device.query('INDEXED_VALUES?') == str(iv)


# check the set_dict_values_property behavior
def check_dict_property(device, key):
    # key must be string or number, set property to include lists, arrays, arbritray values of diversity
    name = device[key]['name']
    ord_dict = OrderedDict(device[key]['dict_values'])
    for k in device[key]['dict_values']:
        device[name] = k
        assert device["_{}".format(name)] == device.find_first_key(ord_dict, ord_dict[k])
        assert device.query('DICT_VALUES?') == device.find_first_key(ord_dict, ord_dict[k])

    for item in BAD_INPUTS:
        if item not in device[key]['dict_values']:
            with pytest.raises(Exception):
                device[name] = item

    with pytest.raises(Exception):
        device[name] = True

def test_driver(device, expected_attributes, expected_values):
    check_has_attributes(device, expected_attributes)

    check_attribute_values(device, expected_attributes, expected_values)


