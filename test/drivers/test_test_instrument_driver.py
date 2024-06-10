# -*- coding: utf-8 -*-
import pytest
import math
import string
from collections import OrderedDict
from pyscan.drivers.testing.test_instrument_driver import TestInstrumentDriver
from pyscan.drivers.testing.auto_test_driver import test_driver

# #################### still need to add error flags for this file...
# ##################### test more thouroughly with multiple instances to make sure
# ######## this works and doesn't bug out like it did with multiple testvoltage instances
# ######### on 2_29_24


def test_testinstrumentdriver():
    test_instrument = TestInstrumentDriver()

    # check that the initialized state has the expected attributes
    def check_has_attributes(device, attributes):
        for a in attributes:
            assert hasattr(test_instrument, a), "test device does not have {} attribute when initialized".format(a)

    attributes = ['instrument', 'debug', '_float_values_settings', '_str_values_settings',
                  '_range_settings', '_indexed_values_settings', '_dict_values_settings', '_float_values',
                  '_str_values', '_range', '_indexed_values', "_dict_values", "_version", "black_list_for_testing"]
    check_has_attributes(test_instrument, attributes)

    # check that the initialized attributes have the expected values
    def check_attribute_values(device, attributes, ev):
        for i in range(len(ev)):
            err_string = "test device {} attribute does not equal {}".format(device[attributes[i]], ev[i])
            assert (device[attributes[i]] == ev[i]), err_string

    floatvs = {'name': 'float_values', 'write_string': 'FLOAT_VALUES {}', 'query_string': 'FLOAT_VALUES?',
               'values': [2, 2.2339340249, 89.129398], 'return_type': float}
    strvs = {'name': 'str_values', 'write_string': 'STR_VALUES {}', 'query_string': 'STR_VALUES?',
             'values': ['2', 'x', 'False', '(1, 10)', "['1', '10']"], 'return_type': str}
    rgs = {'name': 'range', 'write_string': 'RANGE {}', 'query_string': 'RANGE?',
           'range': [0, 10], 'return_type': float}
    idxvs = {'name': 'indexed_values', 'write_string': 'INDEXED_VALUES {}', 'query_string': 'INDEXED_VALUES?',
             'indexed_values': ['A', 'B', 'C', 'D', 196, 2.0, '101001'], 'return_type': str}
    dicts = {'name': 'dict_values', 'write_string': 'DICT_VALUES {}', 'query_string': 'DICT_VALUES?',
             'dict_values': {'on': 1, 'off': 0, '1': 1, '0': 0}, 'return_type': str}
    expected_values = ['instrument#123', False, floatvs, strvs, rgs, idxvs, dicts, 2, '2', 0, 'A', 'off']
    check_attribute_values(test_instrument, attributes, expected_values)

    # check the set_values_property behavior
    def check_values_property(key):
        name = test_instrument[key]['name']
        test_val = 0
        for i in range(-10, 10000):
            if test_val not in test_instrument[key]['values']:
                with pytest.raises(Exception):
                    test_instrument[name] = test_val
            test_val += .1

        with pytest.raises(Exception):
            test_instrument[name] = 'not ok'

        for val in test_instrument[key]['values']:
            test_instrument[name] = val
            assert test_instrument[name] == val, "{} not equal {}".format(test_instrument[name], val)
            assert test_instrument["_{}".format(name)] == val

    # check the set_range_property behavior for a range item
    def check_range_property(key):
        min_range = min(test_instrument[key]['range'])
        max_range = max(test_instrument[key]['range'])
        name = test_instrument[key]['name']
        with pytest.raises(Exception):
            test_instrument[name] = min_range - .001
        with pytest.raises(Exception):
            test_instrument[name] = min_range - 1
        with pytest.raises(Exception):
            test_instrument[name] = max_range + .001
        with pytest.raises(Exception):
            test_instrument[name] = max_range + 1

        # set fixed number of steps to divide the overall range by for step size for actual drivers
        step = 1
        if abs(test_instrument[key]['range'][0] - test_instrument[key]['range'][0]) > 10000:
            step = math.ceil(abs(test_instrument[key]['range'][0] - test_instrument[key]['range'][0]) / 1000)

        for r in range(test_instrument[key]['range'][0], test_instrument[key]['range'][0], step):
            test_instrument[name] = r
            assert test_instrument[name] == r
            assert test_instrument['_{}'.format(name)] == r

    # check the set_indexed_values_property behavior
    def check_indexed_property(key):
        # check a random string rather than a for loop
        name = test_instrument[key]['name']
        for letter in string.ascii_letters:
            if letter not in test_instrument[key]['indexed_values']:
                with pytest.raises(Exception):
                    test_instrument[name] = letter

        step = 0
        for i in range(0, 1000):
            if i not in test_instrument[key]['indexed_values']:
                with pytest.raises(Exception):
                    test_instrument[name] = step
            step += .1

        with pytest.raises(Exception):
            test_instrument[name] = True
        with pytest.raises(Exception):
            test_instrument[name] = [1, 5]
        with pytest.raises(Exception):
            test_instrument[name] = {'key1': 'bad boy', 'key2': 'badder girl'}

        for idx, iv in enumerate(test_instrument._indexed_values_settings['indexed_values']):
            test_instrument[name] = iv
            assert test_instrument["_{}".format(name)] == iv
            assert test_instrument.query('INDEXED_VALUES?') == str(idx)

    # check the set_dict_values_property behavior
    def check_dict_property(key):
        # key must be string or number, set property to include lists, arrays, arbritray values of diversity
        name = test_instrument[key]['name']
        ord_dict = OrderedDict(test_instrument[key]['dict_values'])
        for k in test_instrument[key]['dict_values']:
            test_instrument[name] = k
            assert test_instrument["_{}".format(name)] == test_instrument.find_first_key(ord_dict, ord_dict[k])
            assert test_instrument.query('DICT_VALUES?') == str(test_instrument[key]['dict_values'][k])

        for letter in string.ascii_letters:
            if letter not in test_instrument[key]['dict_values']:
                with pytest.raises(Exception):
                    test_instrument[name] = letter

        step = 0
        for i in range(0, 1000):
            if i not in test_instrument[key]['dict_values']:
                with pytest.raises(Exception):
                    test_instrument[name] = step
            step += .1

        with pytest.raises(Exception):
            test_instrument[name] = True

    # implements above checks for all attributes by type
    def check_properties(test_instrument, num_val_props=2, num_range_props=1,
                         num_idx_vals_props=1, num_dict_vals_props=1, total_att=15):
        # iterate over all attributes to test accordingly using predefined functions
        values_counter, range_counter, idx_vals_counter, dict_vals_counter = 0, 1, 1, 1
        values_idx, range_idx, idx_vals_idx, dict_vals_idx = [], [], [], []
        for key in test_instrument.__dict__.keys():
            try:
                keys = test_instrument[key].keys()
                if ('values' in keys) and ('indexed_' not in keys) and ('dict_' not in keys):
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
        print("{} values {} {} total attributes.".format(len(values_idx), mid_string, values_counter))
        print("{} indexed values {} {} total attributes.".format(len(idx_vals_idx), mid_string, idx_vals_counter))
        print("{} dict values {} {} total attributes.".format(len(dict_vals_idx), mid_string, dict_vals_counter))

        assert num_val_props == len(values_idx)
        assert num_range_props == len(range_idx)
        assert num_idx_vals_props == len(idx_vals_idx)
        assert num_dict_vals_props == len(dict_vals_idx)
        assert range_counter == values_counter == idx_vals_counter == dict_vals_counter == total_att

    check_properties(test_instrument)

    test_driver(test_instrument)
