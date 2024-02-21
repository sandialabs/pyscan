# -*- coding: utf-8 -*-
from pyscan.drivers import InstrumentDriver
import pytest
import math
import string
from collections import OrderedDict


class TestInstrumentDriver(InstrumentDriver):
    '''Class that exhausts the possible properties of instrument driver to test instrument driver.

    Properties
    ----------
    values :
        for testing values property
    range :
        for testing range property
    ranges :
        for testing ranges property
    indexed_values :
        for testing indexed_values property
    dict_values :
        for testing dict_values property
    '''

    def __init__(self, debug=False, instrument=None, *arg, **kwarg):

        super().__init__(instrument=None, *arg, **kwarg)
        self.initialize_properties()

        self.debug = debug
        self._values = 1
        self._range = 0
        self._ranges = (1, 15)
        self._indexed_values = 'A'
        self._dict_values = 'off'

    def query(self, string):
        if string == 'VALUES?':
            return str(self._values)
        elif string == 'RANGE?':
            return str(self._range)
        elif string == 'RANGES?':
            return str(self._ranges)
        elif string == 'INDEXED_VALUES?':
            return str(self._indexed_values)
        elif string == 'DICT_VALUES?':
            return str(self._dict_values)

    # we are not currently testing for this in test voltage... doesn't seem particularly useful to do so
    def write(self, string):
        if 'VALUES' in string:
            return string.strip('VALUES ')
        elif ('RANGE' in string) and not ('RANGES' in string):
            return string.strip('RANGE ')
        elif 'RANGES' in string:
            return string.strip('RANGES ')
        elif 'INDEXED_VALUES' in string:
            return string.strip('INDEXED_VALUES ')
        elif 'DICT_VALUES' in string:
            return string.strip('DICT_VALUES ')

    def initialize_properties(self):

        self.add_device_property({
            'name': 'values',
            'write_string': 'VALUES {}',
            'query_string': 'VALUES?',
            'values': [1, 10],
            'return_type': int
        })

        self.add_device_property({
            'name': 'range',
            'write_string': 'RANGE {}',
            'query_string': 'RANGE?',
            'range': [0, 10],
            'return_type': float
        })

        self.add_device_property({
            'name': 'ranges',
            'write_string': 'RANGES {}',
            'query_string': 'RANGES?',
            'ranges': ([0, 10], [15, 20]),
            'return_type': float
        })

        self.add_device_property({
            'name': 'indexed_values',
            'write_string': 'INDEXED_VALUES {}',
            'query_string': 'INDEXED_VALUES?',
            'indexed_values': ['A', 'B', 'C', 'D'],
            'return_type': str
        })

        self.add_device_property({
            'name': 'dict_values',
            'write_string': 'DICT_VALUES {}',
            'query_string': 'DICT_VALUES?',
            'dict_values': {'on': 1, 'off': 0, '1': 1, '0': 0},
            'return_type': str
        })
        with pytest.raises(Exception):
            self.add_device_property({
                'name': 'bad_values',
                'write_string': 'DICT_VALUES {}',
                'query_string': 'DICT_VALUES?',
                'invalid_key_name': {'on': 1, 'off': 0, '1': 1, '0': 0},
                'return_type': str
            })


def test_instrumentdriver():
    test_instrument = TestInstrumentDriver()

    # check that the initialized state has the expected attributes
    def check_has_attributes(device, attributes):
        for a in attributes:
            assert hasattr(test_instrument, a), "test device does not have {} attribute when initialized".format(a)

    attributes = ['instrument', 'debug', '_values_settings', '_range_settings', '_ranges_settings',
                  '_indexed_values_settings', '_dict_values_settings', '_values', '_range', '_ranges',
                  '_indexed_values', "_dict_values"]
    check_has_attributes(test_instrument, attributes)

    # check that the initialized attributes have the expected values
    def check_attribute_values(device, attributes, ev):
        for i in range(len(ev)):
            err_string = "test device {} attribute does not equal {}".format(device[attributes[i]], ev[i])
            assert device[attributes[i]] == ev[i], err_string

    vs = {'name': 'values', 'write_string': 'VALUES {}', 'query_string': 'VALUES?',
          'values': [1, 10], 'return_type': int}
    rgs = {'name': 'range', 'write_string': 'RANGE {}', 'query_string': 'RANGE?',
           'range': [0, 10], 'return_type': float}
    rgss = {'name': 'ranges', 'write_string': 'RANGES {}', 'query_string': 'RANGES?',
            'ranges': ([0, 10], [15, 20]), 'return_type': float}
    idxvs = {'name': 'indexed_values', 'write_string': 'INDEXED_VALUES {}', 'query_string': 'INDEXED_VALUES?',
             'indexed_values': ['A', 'B', 'C', 'D'], 'return_type': str}
    dicts = {'name': 'dict_values', 'write_string': 'DICT_VALUES {}', 'query_string': 'DICT_VALUES?',
             'dict_values': {'on': 1, 'off': 0, '1': 1, '0': 0}, 'return_type': str}
    expected_values = [None, False, vs, rgs, rgss, idxvs, dicts, 1, 0, (1, 15), 'A', 'off']
    check_attribute_values(test_instrument, attributes, expected_values)

    # check the set_values_property behavior
    def check_values_property(key):
        print("entered check_values_property()")
        name = test_instrument[key]['name']
        test_val = 0
        for i in range(-10, 10000):
            if test_val not in test_instrument[key]['values']:
                with pytest.raises(Exception):
                    test_instrument[name] = test_val
            test_val += .1

        with pytest.raises(Exception):
            test_instrument.values = 'not ok'
        with pytest.raises(Exception):
            test_instrument.values = False

        for val in test_instrument[key]['values']:
            test_instrument[name] = val
            assert test_instrument["_{}".format(name)] == val
            assert test_instrument.query('VALUES?') == str(val)

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

        step = 1
        if abs(test_instrument[key]['range'][0] - test_instrument[key]['range'][0]) > 10000:
            step = math.ceil(abs(test_instrument[key]['range'][0] - test_instrument[key]['range'][0]) / 1000)

        for r in range(test_instrument[key]['range'][0], test_instrument[key]['range'][0], step):
            test_instrument[name] = r
            assert test_instrument['_{}'.format(name)] == r
            # I do not expect this would be ubiquitous and will likely need to be reconsidered.
            assert test_instrument.query('RANGE?') == str(r)

    # check the set_range_properties behavior
    def check_ranges_property(key):
        min1_range = min(test_instrument[key]['ranges'][0])
        max1_range = max(test_instrument[key]['ranges'][0])
        min2_range = min(test_instrument[key]['ranges'][1])
        max2_range = max(test_instrument[key]['ranges'][1])
        name = test_instrument[key]['name']
        with pytest.raises(Exception):
            test_instrument[name] = 1
        with pytest.raises(Exception):
            test_instrument[name] = (min1_range, min2_range - .001)
        with pytest.raises(Exception):
            test_instrument[name] = (min1_range, min2_range - 1)
        with pytest.raises(Exception):
            test_instrument[name] = (min1_range, max2_range + .001)
        with pytest.raises(Exception):
            test_instrument[name] = (min1_range, max2_range + 1)
        with pytest.raises(Exception):
            test_instrument[name] = (min1_range - .001, min2_range)
        with pytest.raises(Exception):
            test_instrument[name] = (min1_range - 1, min2_range)
        with pytest.raises(Exception):
            test_instrument[name] = (max1_range + .001, min2_range)
        with pytest.raises(Exception):
            test_instrument[name] = (max1_range + 1, min2_range)

        step1, step2 = 1, 1
        if abs(test_instrument[key][name][0][0] - test_instrument[key][name][0][1]) > 1000:
            step1 = math.ceil(abs(test_instrument[key][name][0][0] - test_instrument[key][name][0][1]) / 1000)
        if abs(test_instrument[key][name][1][0] - test_instrument[key][name][1][1]) > 1000:
            step2 = math.ceil(abs(test_instrument[key][name][1][0] - test_instrument[key][name][1][1]) / 1000)
        for r1 in range(test_instrument[key][name][0][0], test_instrument[key][name][0][1], step1):
            for r2 in range(test_instrument[key][name][1][0], test_instrument[key][name][1][1], step2):
                test_instrument.ranges = (r1, r2)
                assert test_instrument._ranges == (r1, r2)
                assert test_instrument.query('RANGES?') == '({}, {})'.format(r1, r2)

    # check the set_indexed_values_property behavior
    def check_indexed_property(key):
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

        for iv in test_instrument._indexed_values_settings['indexed_values']:
            test_instrument[name] = iv
            assert test_instrument["_{}".format(name)] == iv
            assert test_instrument.query('INDEXED_VALUES?') == iv

    # check the set_dict_values_property behavior
    def check_dict_property(key):
        name = test_instrument[key]['name']
        ord_dict = OrderedDict(test_instrument[key]['dict_values'])
        for k in test_instrument[key]['dict_values']:
            test_instrument[name] = k
            assert test_instrument["_{}".format(name)] == test_instrument.find_first_key(ord_dict, ord_dict[k])
            assert test_instrument.query('DICT_VALUES?') == test_instrument.find_first_key(ord_dict, ord_dict[k])

        name = test_instrument[key]['name']
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

    check_dict_property('_dict_values_settings')

    # implements above checks for all attributes by type
    def check_properties(test_instrument, num_val_props=1, num_range_props=1, num_ranges_props=1,
                         num_idx_vals_props=1, num_dict_vals_props=1, total_att=8):
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

    check_properties(test_instrument)

    print("ALL TESTS PASSED BABY!!! WOOT WOOT!!!!!!!!!")


test_instrumentdriver()
