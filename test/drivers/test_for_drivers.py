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


# implements above checks for all attributes by type
def check_properties(test_instrument, num_val_props, num_range_props, num_ranges_props,
                     num_idx_vals_props, num_dict_vals_props, total_att):
    # iterate over all attributes to test accordingly using predefined functions
    values_counter, range_counter, ranges_counter, idx_vals_counter, dict_vals_counter = 0, 0, 0, 0, 0
    values_idx, range_idx, ranges_idx, idx_vals_idx, dict_vals_idx = [], [], [], [], []
    for key in test_instrument.__dict__.keys():
        try:
            if 'values' in test_instrument[key].keys():
                values_counter += 1
                values_idx.append(values_counter)
                check_values_property(key)
        except:
            values_counter += 1
        try:
            if 'range' in test_instrument[key].keys():
                range_counter += 1
                range_idx.append(range_counter)
                check_range_property(key)
        except:
            range_counter += 1
        try:
            if 'ranges' in test_instrument[key].keys():
                ranges_counter += 1
                ranges_idx.append(range_counter)
                check_ranges_property(key)
        except:
            ranges_counter += 1
        try:
            if 'indexed_values' in test_instrument[key].keys():
                idx_vals_counter += 1
                idx_vals_idx.append(idx_vals_counter)
                check_indexed_property(key)
        except:
            idx_vals_counter += 1
        try:
            if 'dict_values' in test_instrument[key].keys():
                dict_vals_counter += 1
                dict_vals_idx.append(dict_vals_counter)
                check_dict_property(key)
        except:
            dict_vals_counter += 1

    mid_string = 'properties found and tested out of'
    print("{} range {} {} total attributes.".format(len(range_idx), mid_string, range_counter))
    print("{} ranges {} {} total attributes.".format(len(ranges_idx), mid_string, ranges_counter))
    print("{} values {} {} total attributes.".format(len(values_idx), mid_string, values_counter))
    print("{} indexed values {} {} total attributes.".format(len(idx_vals_idx), mid_string, idx_vals_counter))
    print("{} dict values {} {} total attributes.".format(len(dict_vals_idx), mid_string, dict_vals_counter))

    assert num_val_props == len(values_idx)
    assert num_range_props == len(range_idx)
    assert num_ranges_props == len(ranges_idx)
    assert num_idx_vals_props == len(idx_vals_idx)
    assert num_dict_vals_props == len(dict_vals_idx)
    assert range_counter == ranges_counter == values_counter == idx_vals_counter == dict_vals_counter == total_att


# implement the above sections to test your drivers properties with the device
def test_driver(device, expected_attributes, expected_values, num_val_props, num_range_props,
                num_ranges_props, num_idx_vals_props, num_dict_vals_props, total_att):
    check_has_attributes(device, expected_attributes)

    check_attribute_values(device, expected_attributes, expected_values)

    check_properties(device, num_val_props, num_range_props, num_ranges_props, num_idx_vals_props,
                     num_dict_vals_props, total_att)
