'''
Pytest functions to test the Runinfo class
'''

import pyscan as ps
import pytest


#  ######## need to add tests for runinfo's different @property definitions.
def test_init_from_noparams():
    """
    Testing init from no paramaters in RunInfo

    Returns
    -------
    None

    """

    init_runinfo = ps.RunInfo()

    # for checking that scans have expected attributes
    def check_scans_have_attribute(scans, attribute_name):
        counter = 0
        for scan in scans:
            err_string = "runinfo scan" + str(counter) + " (Property Scan) " + attribute_name + " not intialized"
            assert hasattr(scan, attribute_name), err_string
            counter += 1

    # for checking that runinfo attributes are as expected
    def check_attribute(runinfo, attribute, attribute_name, expected):
        err_string1 = "runinfo " + attribute_name + " not initialized"
        assert hasattr(runinfo, attribute_name), err_string1
        err_string2 = "runinfo " + attribute_name + " not " + str(expected) + " when intialized"
        assert (attribute is expected or attribute == expected), err_string2

    # check that runinfo scans are initialized correctly
    def check_runinfo_scans():
        # check that scans 0 - 4 initialized
        for i in range(4):
            assert hasattr(init_runinfo, 'scan' + str(i)), "runinfo scan" + str(i) + " not initialized"

        # check that scans 0 - 4 initialized
        for scan in init_runinfo.scans:
            assert isinstance(scan, ps.PropertyScan), "runinfo scans not initialized as Property Scan"

        # check that scan attributes are initialized
        check_scans_have_attribute(init_runinfo.scans, 'scan_dict')
        check_scans_have_attribute(init_runinfo.scans, 'prop')
        check_scans_have_attribute(init_runinfo.scans, 'dt')
        check_scans_have_attribute(init_runinfo.scans, 'i')

        # check that each scans attributes are initialized correctly
        counter = 0
        for scan in init_runinfo.scans:
            # check that scan_dict initialized as empty {}
            err_string = "runinfo scan" + str(counter) + " (Property Scan) scan_dict not empty when intialized"
            assert scan.scan_dict == {}, err_string

            # check that prop initialized as None
            err_string = "runinfo scan" + str(counter) + " (Property Scan) prop not None when intialized"
            assert scan.prop is None, err_string

            # check that dt initialized as 0
            assert scan.dt == 0, "runinfo scan" + str(counter) + " (Property Scan) dt not 0 when intialized"

            # check that i initialized as 0
            assert scan.i == 0, "runinfo scan" + str(counter) + " (Property Scan) i not 0 when intialized"

            counter += 1

    check_runinfo_scans()

    # check that runinfo attributes are initialized correctly
    def check_runinfo_attributes():
        # check that static initialized correctly
        check_attribute(runinfo=init_runinfo, attribute=init_runinfo.static, attribute_name='static', expected={})

        # check that measured initialized correctly
        check_attribute(runinfo=init_runinfo, attribute=init_runinfo.measured, attribute_name='measured', expected=[])

        # check that measure_function initialized correctly
        check_attribute(runinfo=init_runinfo, attribute=init_runinfo.measure_function,
                        attribute_name='measure_function', expected=None)

        # check that trigger_function initialized correctly
        check_attribute(runinfo=init_runinfo, attribute=init_runinfo.trigger_function,
                        attribute_name='trigger_function', expected=None)

        # check that initial_pause initialized correctly
        check_attribute(runinfo=init_runinfo, attribute=init_runinfo.initial_pause,
                        attribute_name='initial_pause', expected=0.1)

        # check that average_d initialized correctly
        check_attribute(runinfo=init_runinfo, attribute=init_runinfo.average_d, attribute_name='average_d', expected=-1)

        # check that verbose initialized correctly
        check_attribute(runinfo=init_runinfo, attribute=init_runinfo.verbose, attribute_name='verbose', expected=False)

    check_runinfo_attributes()

    init_runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    init_runinfo.scan1 = ps.PropertyScan({'v2': ps.drange(0, 0.1, 0.1)}, 'voltage')
    init_runinfo.check()
    with pytest.raises(Exception):
        init_runinfo.scan3 = ps.PropertyScan({'v3': ps.drange(0, 0.1, 0.1)}, 'voltage')
        init_runinfo.check()
