'''
Pytest functions to test the Scans class
'''


import pyscan as ps
import numpy as np
import pytest
from time import sleep


# for checking that the scans have the given attributes
def check_has_attributes(scan, scan_name, attribute_names):
    for i in attribute_names:
        err_string = scan_name + " scan " + i + " not intialized"
        assert hasattr(scan, i), err_string


# for checking that the scans have the expected attribute values
def check_attribute_value(scan_name, attribute_name, attribute, expected_value):
    err_string = scan_name + " scan " + attribute_name + " not " + str(expected_value) + " when intialized"
    assert attribute == expected_value, err_string


# for checking that the iterate function is working as expected
def check_iterate_function(scan, scan_name, devices=[]):
    # check that iterate is callable
    assert callable(scan.iterate), scan_name + " scan iterate function not callable"

    # check that iterate functions as expected
    try:
        scan.iterate(0, devices)  # This only tests if it runs, not if the results are desired.
    except Exception:
        assert False, scan_name + " scan iterate function error"


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

    # set up basic scan
    # scan = ps.MetaScan(0, [])

    # scan_name = 'MetaScan'

    # ensure empty scan is instance of Property Scan
    # assert isinstance(scan, ps.MetaScan), scan_name + " scan not initialized as MetaScan"

    assert True


def test_property_scan():
    """
    Testing property scan, with both 0D and 1D inputs

    Returns
    --------
    None
    """

    # for testing a property scan scan initialized as empty
    def test_empty_scan():
        # set up empty scan
        scan = ps.PropertyScan({}, prop=None)

        scan_name = 'Property Scan empty'

        # ensure empty scan is instance of Property Scan
        assert isinstance(scan, ps.PropertyScan), scan_name + " scan not initialized as Property Scan"

        # check that the empty scan attributes are initialized
        attribute_names = ['device_names', 'scan_dict', 'input_dict', 'prop', 'dt', 'i', 'n']
        check_has_attributes(scan, scan_name, attribute_names)

        # check the attributes are initialized correctly
        def check_attributes(scan):
            # check that device_names initialized with correct value
            check_attribute_value(scan_name, 'device names', scan.device_names, expected_value=[])

            # check that scan_dict has the expected number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(scan.scan_dict.keys())), expected_value=0)

            # check same length function is callable and passes
            err_string1 = scan_name + " scan check same length not callable"
            assert callable(scan.check_same_length), err_string1
            err_string2 = scan_name + " scan check same length failed"
            assert scan.check_same_length, err_string2

            # check that n has the expected value
            check_attribute_value(scan_name, 'n', scan.n, expected_value=1)

            # check that scan_dict initialized correctly
            check_attribute_value(scan_name, 'scan_dict', scan.scan_dict, expected_value={})

            # check that prop initialized with correct value
            err_string = "Property Scan empty scan prop not None when intialized"
            assert scan.prop is None, err_string

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', scan.dt, expected_value=0)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', scan.i, expected_value=0)

            # check that iterate functions as expected
            check_iterate_function(scan, scan_name)

        check_attributes(scan)

    # test a property scan scan initialized as empty
    test_empty_scan()

    def test_1D_property_scan_4scans():
        # set up 4 scans as "scans" to test
        scans = [0, 1, 2, 3]
        self = ['v1', 'v2', 'v3', 'v4']
        prop = 'voltage'
        scans[0] = ps.PropertyScan({self[0]: ps.drange(0, 0.1, 0.1)}, prop, dt=.01)
        scans[1] = ps.PropertyScan({self[1]: ps.drange(0.1, 0.1, 0)}, prop, dt=.01)
        scans[2] = ps.PropertyScan({self[2]: ps.drange(0.3, 0.1, 0.2)}, prop, dt=.01)
        scans[3] = ps.PropertyScan({self[3]: ps.drange(-0.1, 0.1, 0)}, prop, dt=.01)

        # verifying the check same length function called by property scan will fail with bad runinfo
        with pytest.raises(Exception):
            bad_runinfo = ps.RunInfo()
            bad_runinfo.scan1 = ps.PropertyScan({'v1': ps.drange(5, 5, 5), 'diff': ps.drange(0, 0.1, 0.1)}, 'voltage')

        # setup devices for testing iterate function
        devices = setup_devices()

        scan_name = "Property Scan scan"

        # check that scans 0 - 4 initialized as Property Scan
        counter = 0
        for scan in scans:
            assert isinstance(scan, ps.PropertyScan), "scan" + str(counter) + " not initialized as Property Scan"
            counter += 1

        # for checking that scans as scans have expected attributes
        def check_scans_have_attribute(scans, attribute_name):
            counter = 0
            for scan in scans:
                err_string = "scan" + str(counter) + " (Property Scan) " + attribute_name + " not intialized"
                assert hasattr(scan, attribute_name), err_string
                counter += 1

        # check that scan attributes are initialized
        check_scans_have_attribute(scans, 'device_names')
        check_scans_have_attribute(scans, 'scan_dict')
        check_scans_have_attribute(scans, 'input_dict')
        check_scans_have_attribute(scans, 'prop')
        check_scans_have_attribute(scans, 'dt')
        check_scans_have_attribute(scans, 'i')
        check_scans_have_attribute(scans, 'n')

        # for checking that scans as scans attribute values are correct
        def check_scan_attributes(scans, scan_num, self, prop,
                                  expected_scan_dict1, expected_scan_dict2, expected_dt, expected_i):
            # check that device_names initialized with correct value
            err_string = "Property Scan scan" + str(scan_num) + " device names not " + self
            assert scans[scan_num].device_names == [self]

            # check that scan_dict has the right number of keys
            err_string1 = "Property Scan scan" + str(scan_num) + " scan_dict has no keys"
            err_string2 = "Property Scan scan" + str(scan_num) + " scan_dict num keys not 1"
            assert len(list(scans[scan_num].scan_dict.keys())) > 0, err_string1
            assert len(list(scans[scan_num].scan_dict.keys())) == 1, err_string2

            # check same length and that n is right value
            err_string1 = "Property Scan scan" + str(scan_num) + " check same length failed"
            err_string2 = "Property Scan scan" + str(scan_num) + " n not 2"
            assert scans[scan_num].check_same_length, err_string1
            assert scans[scan_num].n == 2, err_string2

            # check that scan_dict initialized with correct values
            prestring = "Property Scan scan" + str(scan_num) + " scan_dict " + self + "_" + prop
            err_string1 = prestring + "[0] not " + str(expected_scan_dict1) + " when initialized"
            err_string2 = prestring + "[1] not " + str(expected_scan_dict1) + " when initialized"
            assert scans[scan_num].scan_dict[self + "_" + prop][0] == expected_scan_dict1, err_string1
            assert scans[scan_num].scan_dict[self + "_" + prop][1] == expected_scan_dict2, err_string2

            # check that prop initialized with correct value
            err_string = "Property Scan scan" + str(scan_num) + " prop not " + prop + " when intialized"
            assert scans[scan_num].prop == prop, err_string

            # check that dt initialized with correct value
            err_string = "Property Scan scan" + str(scan_num) + " dt not " + str(expected_dt) + " when intialized"
            assert scans[scan_num].dt == expected_dt, err_string

            # check that i initialized with correct value
            err_string = "Property Scan scan" + str(scan_num) + " i not " + str(expected_i) + " when intialized"
            assert scans[scan_num].i == expected_i, err_string

            # check that iterate functions as expected (this adds a lot of runtime to the testing)
            for scan in scans:
                check_iterate_function(scan, scan_name)

                for m in range(scan.n):
                    scan.iterate(scan.i, devices)

                    for dev in scan.device_names:
                        devices[dev][scan.prop] == scan.scan_dict[dev + '_' + scan.prop][scan.i]

                    sleep(scan.dt)  # Can we remove this to save time when running test cases, or is it important?

        # check each scan for expected attribute values
        check_scan_attributes(scans, 0, self[0], prop, expected_scan_dict1=0.0,
                              expected_scan_dict2=0.1, expected_dt=.01, expected_i=0)
        check_scan_attributes(scans, 1, self[1], prop, expected_scan_dict1=0.1,
                              expected_scan_dict2=0.0, expected_dt=.01, expected_i=0)
        check_scan_attributes(scans, 2, self[2], prop, expected_scan_dict1=0.3,
                              expected_scan_dict2=0.2, expected_dt=.01, expected_i=0)
        check_scan_attributes(scans, 3, self[3], prop, expected_scan_dict1=-0.1,
                              expected_scan_dict2=0.0, expected_dt=.01, expected_i=0)

    test_1D_property_scan_4scans()

    # ########are we intending to test multi dictionary input items for scans and should I add test cases for them here?


def test_function_scan():
    """
    Testing function scan, with both populated and unpopulated inputs

    Returns
    --------
    None
    """

    # for testing a function scan scan initialized as empty
    def test_empty_scan():
        def input_function():
            pass

        # initialize the empty function scan scan
        scan = ps.FunctionScan(input_function, values=[])

        scan_name = 'Function Scan empty'

        # ensure empty scan is instance of Function Scan
        assert isinstance(scan, ps.FunctionScan), "empty scan not initialized as Function Scan"

        # check that the empty scan attributes are initialized
        attribute_names = ['scan_dict', 'function', 'dt', 'i', 'n']
        check_has_attributes(scan, scan_name, attribute_names)

        # check that the attributes are initialized correctly
        def check_attributes():
            # check that scan_dict has the right number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(scan.scan_dict.keys())), expected_value=1)

            # check that scan_dict initialized correctly
            check_attribute_value(scan_name, 'scan_dict', scan.scan_dict, expected_value={'input_function': []})

            # check that function is callable
            err_string = scan_name + " scans function not a callable function"
            assert callable(scan.function), err_string

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', scan.dt, expected_value=0)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', scan.i, expected_value=0)

            # check that n initialized with correct value
            check_attribute_value(scan_name, 'n', scan.n, expected_value=0)

            # check that iterate is callable
            assert callable(scan.iterate), scan_name + " scan iterate function not callable"

            # check that running the iterate function on empty function scan with no index fails
            with pytest.raises(Exception):
                check_iterate_function(scan, scan_name)

        check_attributes()

    # test a function scan scan initialized as empty
    test_empty_scan()

    # for testing a function scan scan initialized as populated
    def test_scan(return_value=0):
        # set up a basic function to pass as an input to the function scan
        def input_function(num):
            for i in range(num):
                pass
            return return_value

        # setup devices for testing iterate function
        devices = setup_devices()

        # initialize the function scan scan
        scan = ps.FunctionScan(input_function, values=[0, 1, 2], dt=.1)

        scan_name = 'Function Scan populated'

        # ensure scan is instance of Function Scan
        assert isinstance(scan, ps.FunctionScan), "populated scan not initialized as Function Scan"

        # check that the scan attributes are initialized
        attribute_names = ['scan_dict', 'function', 'dt', 'i', 'n']
        check_has_attributes(scan, scan_name, attribute_names)

        # for checking that the attributes are initialized correctly
        def check_attributes():
            # check that scan_dict has the right number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(scan.scan_dict.keys())), expected_value=1)

            # check that scan_dict initialized correctly
            check_attribute_value(scan_name, 'scan_dict', scan.scan_dict, expected_value={'input_function': [0, 1, 2]})

            # check that function initialized correctly
            err_string = scan_name + " scan function not a callable function"
            assert callable(scan.function), err_string

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', scan.dt, expected_value=.1)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', scan.i, expected_value=0)

            # check that n initialized with correct value
            check_attribute_value(scan_name, 'n', scan.n, expected_value=3)

            # check that iterate functions as expected
            check_iterate_function(scan, scan_name, devices=devices)
            err_string = scan_name + " iterate function not as expected."
            assert scan.function(scan.scan_dict[scan.function.__name__][0]) == return_value, err_string

        # check that the attributes are initialized correctly
        check_attributes()

    # test a function scan scan initialized as populated
    test_scan()
    test_scan(return_value=1)


def test_repeat_scan():
    """
    Testing repeat scan, with various numbers of repeats

    Returns
    --------
    None
    """

    # for testing repeat scans with different numbers of repeats
    def test_num_repeat(num_repeat, dt=0):
        # initialize the repeat scan scan
        scan = ps.RepeatScan(num_repeat, dt=dt)

        scan_name = 'Repeat Scan with ' + str(num_repeat) + ' num repeats'

        # check that the empty scan attributes are initialized
        attribute_names = ['device_names', 'scan_dict', 'dt', 'i', 'n']
        check_has_attributes(scan, scan_name, attribute_names)

        # check the attributes are initialized correctly
        def check_attributes(scan, dt=0):
            # check that device_names initialized with correct value
            check_attribute_value(scan_name, 'device names', scan.device_names, expected_value=['repeat'])

            # check that scan_dict has the right number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(scan.scan_dict.keys())), expected_value=1)

            # check same length placeholder
            err_string = scan_name + " check same length failed"
            assert scan.check_same_length, err_string

            # check that n initialized correctly depending on if num_repeat is infinity or not
            if (num_repeat is not np.inf):
                check_attribute_value(scan_name, 'n', scan.n, expected_value=num_repeat)

            else:
                check_attribute_value(scan_name, 'n', scan.n, expected_value=0)

            # check that scan_dict initialized correctly depending on if num_repeat is infinity or not
            if (num_repeat is not np.inf):
                check_attribute_value(scan_name, 'scan_dict', scan.scan_dict,
                                      expected_value={'repeat': list(range(num_repeat))})
            else:
                check_attribute_value(scan_name, 'scan_dict', scan.scan_dict, expected_value={'repeat': []})

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', scan.dt, expected_value=dt)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', scan.i, expected_value=0)

            # check that iterate functions as expected
            check_iterate_function(scan, scan_name)

        check_attributes(scan, dt)

    with pytest.raises(Exception):
        test_num_repeat(-1), "Repeat scan num repeats can be negative when it is not allowed"
    with pytest.raises(Exception):
        test_num_repeat(0), "Repeat scan num repeats can be 0 when it is not allowed"
    test_num_repeat(1)
    test_num_repeat(1, dt=.1)
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

    # for testing average scans with different number of times to average data from inner scans
    def test_num_average(n_average, dt=0):
        # initialize the average scan scan
        scan = ps.AverageScan(n_average, dt)

        scan_name = 'Average Scan with ' + str(n_average) + ' n_average'

        # check that the empty scan attributes are initialized
        attribute_names = ['device_names', 'scan_dict', 'dt', 'i', 'n']
        check_has_attributes(scan, scan_name, attribute_names)

        # check the attributes are initialized correctly
        def check_attributes(scan, dt=0):
            # check that device_names initialized with correct value
            check_attribute_value(scan_name, 'device names', scan.device_names, expected_value=['average'])

            # check that scan_dict has the right number of keys
            check_attribute_value(scan_name, 'scan_dict num keys', len(list(scan.scan_dict.keys())), expected_value=1)

            # check same length placeholder
            err_string = scan_name + " check same length failed"
            assert scan.check_same_length, err_string

            # check that n initialized correctly
            check_attribute_value(scan_name, 'n', scan.n, expected_value=n_average)

            # check that scan_dict initialized correctly
            check_attribute_value(scan_name, 'scan_dict', scan.scan_dict,
                                  expected_value={'average': list(scan.iterator())})

            # check that dt initialized with correct value
            check_attribute_value(scan_name, 'dt', scan.dt, expected_value=dt)

            # check that i initialized with correct value
            check_attribute_value(scan_name, 'i', scan.i, expected_value=0)

            # check that iterate functions as expected
            check_iterate_function(scan, scan_name)

        check_attributes(scan, dt)

    with pytest.raises(Exception):
        test_num_average(-1), "Average Scan n_average can be negative when it should be 1 or more"
    with pytest.raises(Exception):
        test_num_average(0), "Average Scan n_average can be 0 when it should be 1 or more"
    test_num_average(1)
    test_num_average(2)
    test_num_average(2, dt=.1)
    test_num_average(100)
    with pytest.raises(Exception):
        test_num_average(np.inf), "Average Scan n_average can be np.inf when it is not allowed"
