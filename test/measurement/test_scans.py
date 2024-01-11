'''
Pytest functions to test the Scans class
'''

import pyscan as ps
import numpy as np
import pytest
from time import sleep


# for checking that the scans have the given attributes
def check_has_attributes(loop, scan_name, attribute_names):
    for i in attribute_names:
        err_string = scan_name + " loop " + i + " not intialized"
        assert hasattr(loop, i), err_string


# for checking that the scans have the expected attribute values
def check_attribute_value(scan_name, attribute_name, attribute, expected_value):
    err_string = scan_name + " loop " + attribute_name + " not " + str(expected_value) + " when intialized"
    assert attribute == expected_value, err_string


# for checking that the iterate function is working as expected
def check_iterate_function(loop, scan_name, devices=[]):
    # check that iterate is callable
    assert callable(loop.iterate), scan_name + " loop iterate function not callable"

    # check that iterate functions as expected
    try:
        loop.iterate(0, devices)  # This only tests if it runs, not if the results are desired.
    except Exception:
        assert False, scan_name + " loop iterate function error"


# for setting up devices to test scans iterate functions
def setup_devices():
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    devices.v3 = ps.TestVoltage()
    devices.v4 = ps.TestVoltage()
    return devices


# mostly a placeholder for now, meta scan has no init function
def test_meta_scan():
    """
    Testing function scan

    Returns
    --------
    None
    """

    # set up basic loop
    # loop = ps.MetaScan(0, [])

    # scan_name = 'MetaScan'

    # ensure empty loop is instance of Property Scan
    # assert isinstance(loop, ps.MetaScan), scan_name + " loop not initialized as MetaScan"

    assert True


def test_property_scan():
    """
    Testing property scan, with both 0D and 1D inputs

    Returns
    --------
    None
    """

    # for testing a property scan loop initialized as empty
    def test_empty_loop():
        # set up empty loop
        loop = ps.PropertyScan({}, prop=None)

        scan_name = 'Property Scan empty'

        # ensure empty loop is instance of Property Scan
        assert isinstance(loop, ps.PropertyScan), scan_name + " loop not initialized as Property Scan"

        # check that the empty loop attributes are initialized
        attribute_names = ['device_names', 'scan_dict', 'input_dict', 'prop', 'dt', 'i', 'n']
        check_has_attributes(loop, scan_name, attribute_names)

        # check the attributes are initialized correctly
        def check_attributes(loop):
            # check that device_names initialized with correct value
            check_attribute_value(scan_name, 'device names', loop.device_names, expected_value=[])

            # check that scan_dict has the expected number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(loop.scan_dict.keys())), expected_value=0)

            # check same length function is callable and passes
            err_string1 = scan_name + " loop check same length not callable"
            assert callable(loop.check_same_length), err_string1
            err_string2 = scan_name + " loop check same length failed"
            assert loop.check_same_length, err_string2

            # check that n has the expected value
            check_attribute_value(scan_name, 'n', loop.n, expected_value=1)

            # check that scan_dict initialized correctly
            check_attribute_value(scan_name, 'scan_dict', loop.scan_dict, expected_value={})

            # check that prop initialized with correct value
            err_string = "Property Scan empty loop prop not None when intialized"
            assert loop.prop is None, err_string

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', loop.dt, expected_value=0)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', loop.i, expected_value=0)

            # check that iterate functions as expected
            check_iterate_function(loop, scan_name)

        check_attributes(loop)

    # test a property scan loop initialized as empty
    test_empty_loop()

    def test_1D_property_scan_4loops():
        # set up 4 scans as "loops" to test
        loops = [0, 1, 2, 3]
        self = ['v1', 'v2', 'v3', 'v4']
        prop = 'voltage'
        loops[0] = ps.PropertyScan({self[0]: ps.drange(0, 0.1, 0.1)}, prop, dt=.1)
        loops[1] = ps.PropertyScan({self[1]: ps.drange(0.1, 0.1, 0)}, prop, dt=.1)
        loops[2] = ps.PropertyScan({self[2]: ps.drange(0.3, 0.1, 0.2)}, prop, dt=.1)
        loops[3] = ps.PropertyScan({self[3]: ps.drange(-0.1, 0.1, 0)}, prop, dt=.1)

        # setup devices for testing iterate function
        devices = setup_devices()

        scan_name = "Property Scan loop"

        # check that loops 0 - 4 initialized as Property Scan
        counter = 0
        for loop in loops:
            assert isinstance(loop, ps.PropertyScan), "loop" + str(counter) + " not initialized as Property Scan"
            counter += 1

        # for checking that scans as loops have expected attributes
        def check_loops_have_attribute(loops, attribute_name):
            counter = 0
            for loop in loops:
                err_string = "loop" + str(counter) + " (Property Scan) " + attribute_name + " not intialized"
                assert hasattr(loop, attribute_name), err_string
                counter += 1

        # check that loop attributes are initialized
        check_loops_have_attribute(loops, 'device_names')
        check_loops_have_attribute(loops, 'scan_dict')
        check_loops_have_attribute(loops, 'input_dict')
        check_loops_have_attribute(loops, 'prop')
        check_loops_have_attribute(loops, 'dt')
        check_loops_have_attribute(loops, 'i')
        check_loops_have_attribute(loops, 'n')

        # for checking that scans as loops attribute values are correct
        def check_loop_attributes(loops, loop_num, self, prop,
                                  expected_scan_dict1, expected_scan_dict2, expected_dt, expected_i):
            # check that device_names initialized with correct value
            err_string = "Property Scan loop" + str(loop_num) + " device names not " + self
            assert loops[loop_num].device_names == [self]

            # check that scan_dict has the right number of keys
            err_string1 = "Property Scan loop" + str(loop_num) + " scan_dict has no keys"
            err_string2 = "Property Scan loop" + str(loop_num) + " scan_dict num keys not 1"
            assert len(list(loops[loop_num].scan_dict.keys())) > 0, err_string1
            assert len(list(loops[loop_num].scan_dict.keys())) == 1, err_string2

            # check same length and that n is right value
            err_string1 = "Property Scan loop" + str(loop_num) + " check same length failed"
            err_string2 = "Property Scan loop" + str(loop_num) + " n not 2"
            assert loops[loop_num].check_same_length, err_string1
            assert loops[loop_num].n == 2, err_string2

            # check that scan_dict initialized with correct values
            prestring = "Property Scan loop" + str(loop_num) + " scan_dict " + self + "_" + prop
            err_string1 = prestring + "[0] not " + str(expected_scan_dict1) + " when initialized"
            err_string2 = prestring + "[1] not " + str(expected_scan_dict1) + " when initialized"
            assert loops[loop_num].scan_dict[self + "_" + prop][0] == expected_scan_dict1, err_string1
            assert loops[loop_num].scan_dict[self + "_" + prop][1] == expected_scan_dict2, err_string2

            # check that prop initialized with correct value
            err_string = "Property Scan loop" + str(loop_num) + " prop not " + prop + " when intialized"
            assert loops[loop_num].prop == prop, err_string

            # check that dt initialized with correct value
            err_string = "Property Scan loop" + str(loop_num) + " dt not " + str(expected_dt) + " when intialized"
            assert loops[loop_num].dt == expected_dt, err_string

            # check that i initialized with correct value
            err_string = "Property Scan loop" + str(loop_num) + " i not " + str(expected_i) + " when intialized"
            assert loops[loop_num].i == expected_i, err_string

            # check that iterate functions as expected (this adds a lot of runtime to the testing)
            for loop in loops:
                check_iterate_function(loop, scan_name)

                for m in range(loop.n):
                    loop.iterate(loop.i, devices)

                    for dev in loop.device_names:
                        devices[dev][loop.prop] == loop.scan_dict[dev + '_' + loop.prop][loop.i]

                    sleep(loop.dt)  # Can we remove this to save time when running test cases, or is it important?

        # check each loop for expected attribute values
        check_loop_attributes(loops, 0, self[0], prop, expected_scan_dict1=0.0,
                              expected_scan_dict2=0.1, expected_dt=.1, expected_i=0)
        check_loop_attributes(loops, 1, self[1], prop, expected_scan_dict1=0.1,
                              expected_scan_dict2=0.0, expected_dt=.1, expected_i=0)
        check_loop_attributes(loops, 2, self[2], prop, expected_scan_dict1=0.3,
                              expected_scan_dict2=0.2, expected_dt=.1, expected_i=0)
        check_loop_attributes(loops, 3, self[3], prop, expected_scan_dict1=-0.1,
                              expected_scan_dict2=0.0, expected_dt=.1, expected_i=0)

    test_1D_property_scan_4loops()

    # ########are we intending to test multi dictionary input items for loops and should I add test cases for them here?


def test_function_scan():
    """
    Testing function scan, with both populated and unpopulated inputs

    Returns
    --------
    None
    """

    # for testing a function scan loop initialized as empty
    def test_empty_loop():
        def input_function():
            pass

        # initialize the empty function scan loop
        loop = ps.FunctionScan(input_function, values=[])

        scan_name = 'Function Scan empty'

        # ensure empty loop is instance of Function Scan
        assert isinstance(loop, ps.FunctionScan), "empty loop not initialized as Function Scan"

        # check that the empty loop attributes are initialized
        attribute_names = ['scan_dict', 'function', 'dt', 'i', 'n']
        check_has_attributes(loop, scan_name, attribute_names)

        # check that the attributes are initialized correctly
        def check_attributes():
            # check that scan_dict has the right number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(loop.scan_dict.keys())), expected_value=1)

            # check that scan_dict initialized correctly
            check_attribute_value(scan_name, 'scan_dict', loop.scan_dict, expected_value={'input_function': []})

            # check that function is callable
            err_string = scan_name + " loops function not a callable function"
            assert callable(loop.function), err_string

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', loop.dt, expected_value=0)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', loop.i, expected_value=0)

            # check that n initialized with correct value
            check_attribute_value(scan_name, 'n', loop.n, expected_value=0)

            # check that iterate is callable
            assert callable(loop.iterate), scan_name + " loop iterate function not callable"

            # check that running the iterate function on empty function scan with no index fails
            with pytest.raises(Exception):
                check_iterate_function(loop, scan_name)

        check_attributes()

    # test a function scan loop initialized as empty
    test_empty_loop()

    # for testing a function scan loop initialized as populated
    def test_loop(return_value=0):
        # set up a basic function to pass as an input to the function scan
        def input_function(num):
            for i in range(num):
                pass
            return return_value

        # setup devices for testing iterate function
        devices = setup_devices()

        # initialize the function scan loop
        loop = ps.FunctionScan(input_function, values=[0, 1, 2], dt=1)

        scan_name = 'Function Scan populated'

        # ensure loop is instance of Function Scan
        assert isinstance(loop, ps.FunctionScan), "populated loop not initialized as Function Scan"

        # check that the loop attributes are initialized
        attribute_names = ['scan_dict', 'function', 'dt', 'i', 'n']
        check_has_attributes(loop, scan_name, attribute_names)

        # for checking that the attributes are initialized correctly
        def check_attributes():
            # check that scan_dict has the right number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(loop.scan_dict.keys())), expected_value=1)

            # check that scan_dict initialized correctly
            check_attribute_value(scan_name, 'scan_dict', loop.scan_dict, expected_value={'input_function': [0, 1, 2]})

            # check that function initialized correctly
            err_string = scan_name + " loop function not a callable function"
            assert callable(loop.function), err_string

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', loop.dt, expected_value=1)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', loop.i, expected_value=0)

            # check that n initialized with correct value
            check_attribute_value(scan_name, 'n', loop.n, expected_value=3)

            # check that iterate functions as expected
            check_iterate_function(loop, scan_name, devices=devices)
            err_string = scan_name + " iterate function not as expected."
            assert loop.function(loop.scan_dict[loop.function.__name__][0]) == return_value, err_string

        # check that the attributes are initialized correctly
        check_attributes()

    # test a function scan loop initialized as populated
    test_loop()
    test_loop(return_value=1)


def test_repeat_scan():
    """
    Testing repeat scan, with various numbers of repeats

    Returns
    --------
    None
    """

    # for testing repeat scans with different numbers of repeats
    def test_num_repeat(num_repeat, dt=0):
        # initialize the repeat scan loop
        loop = ps.RepeatScan(num_repeat, dt=dt)

        scan_name = 'Repeat Scan with ' + str(num_repeat) + ' num repeats'

        # check that the empty loop attributes are initialized
        attribute_names = ['device_names', 'scan_dict', 'dt', 'i', 'n', 'nrange']
        check_has_attributes(loop, scan_name, attribute_names)

        # check the attributes are initialized correctly
        def check_attributes(loop, dt=0):
            # check that device_names initialized with correct value
            check_attribute_value(scan_name, 'device names', loop.device_names, expected_value=['repeat'])

            # check that scan_dict has the right number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(loop.scan_dict.keys())), expected_value=1)

            # check same length placeholder
            err_string = scan_name + " check same length failed"
            assert loop.check_same_length, err_string

            # check that n initialized correctly depending on if num_repeat is infinity or not
            if (num_repeat is not np.inf):
                check_attribute_value(scan_name, 'n', loop.n, expected_value=num_repeat)

            else:
                check_attribute_value(scan_name, 'n', loop.n, expected_value=0)

            # check that scan_dict initialized correctly depending on if num_repeat is infinity or not
            if (num_repeat is not np.inf):
                check_attribute_value(scan_name, 'scan_dict', loop.scan_dict,
                                      expected_value={'repeat': list(range(num_repeat))})
            else:
                check_attribute_value(scan_name, 'scan_dict', loop.scan_dict, expected_value={'repeat': []})

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', loop.dt, expected_value=dt)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', loop.i, expected_value=0)

            # check that iterate functions as expected
            check_iterate_function(loop, scan_name)

        check_attributes(loop, dt)

    with pytest.raises(Exception):
        test_num_repeat(-1), "Repeat scan num repeats can be negative when it is not allowed"
    with pytest.raises(Exception):
        test_num_repeat(0), "Repeat scan num repeats can be 0 when it is not allowed"
    test_num_repeat(1)
    test_num_repeat(1, dt=1)
    test_num_repeat(1000000)
    with pytest.raises(Exception):
        test_num_repeat(np.inf), "Repeat scan num repeats can be np.inf when it is not allowed"


def test_average_scan():
    """
    Testing average scan, with both populated and unpopulated inputs

    Returns
    --------
    None
    """

    # for testing average scans with different number of times to average data from inner loops
    def test_num_average(n_average, dt=0):
        # initialize the average scan loop
        loop = ps.AverageScan(n_average, dt)

        scan_name = 'Average Scan with ' + str(n_average) + ' n_average'

        # check that the empty loop attributes are initialized
        attribute_names = ['device_names', 'scan_dict', 'dt', 'i', 'n', 'nrange']
        check_has_attributes(loop, scan_name, attribute_names)

        # check the attributes are initialized correctly
        def check_attributes(loop, dt=0):
            # check that device_names initialized with correct value
            check_attribute_value(scan_name, 'device names', loop.device_names, expected_value=['average'])

            # check that scan_dict has the right number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(loop.scan_dict.keys())), expected_value=1)

            # check same length placeholder
            err_string = scan_name + " check same length failed"
            assert loop.check_same_length, err_string

            # check that n initialized correctly
            check_attribute_value(scan_name, 'n', loop.n, expected_value=n_average)

            # check that nrange initialized correctly
            check_attribute_value(scan_name, 'nrange', loop.nrange, expected_value=range(n_average))

            # check that scan_dict initialized correctly
            check_attribute_value(scan_name, 'scan_dict', loop.scan_dict, expected_value={'average': list(loop.nrange)})

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', loop.dt, expected_value=dt)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', loop.i, expected_value=0)

            # check that iterate functions as expected
            check_iterate_function(loop, scan_name)

        check_attributes(loop, dt)

    with pytest.raises(Exception):
        test_num_average(-1), "Average Scan n_average can be negative when it is not allowed"
    with pytest.raises(Exception):
        test_num_average(0), "Average Scan n_average can be 0 when it is not allowed"
    test_num_average(1)
    test_num_average(1, dt=1)
    test_num_average(100)
    with pytest.raises(Exception):
        test_num_average(np.inf), "Average Scan n_average can be np.inf when it is not allowed"
