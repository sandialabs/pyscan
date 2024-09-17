'''
Pytest functions to test the Runinfo class
'''

import pyscan as ps
import pytest
from pyscan.measurement.run_info import drop


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

    # for checking that runinfo attributes are as expected
    def check_attribute(runinfo, attribute, attribute_name, expected):
        err_string1 = "runinfo " + attribute_name + " not initialized"
        assert hasattr(runinfo, attribute_name), err_string1
        err_string2 = "runinfo " + attribute_name + " not " + str(expected) + " when intialized"
        assert (attribute is expected or attribute == expected), err_string2

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

    def check_runinfo_at_properties():
        assert type(init_runinfo.dims) is tuple, "runinfo.dims not initialized as tuple"
        assert len(init_runinfo.dims) == 0, "runinfo.dims not initialized as empty"

        assert type(init_runinfo.average_dims) is tuple, "runinfo.average_dims not initialized as tuple"
        assert len(init_runinfo.average_dims) == 0, "runinfo.average_dims not initialized as empty"

        assert type(init_runinfo.ndim) is int, "runinfo.ndim not initialized as int"
        assert init_runinfo.ndim == 0, "runinfo.ndim not initialized as 0"

        assert type(init_runinfo.n_average_dim) is int, "runinfo.n_average_dim not initialized as int"
        assert init_runinfo.n_average_dim == 0, "runinfo.n_average_dim not initialized as 0"

        assert type(init_runinfo.indicies) is tuple, "runinfo.indicies not initialized as tuple"
        assert len(init_runinfo.indicies) == 0, "runinfo.indicies not initialized as empty"

        assert type(init_runinfo.line_indicies) is tuple, "runinfo.line_indicies not initialized as tuple"
        assert len(init_runinfo.line_indicies) == 0, "runinfo.line_indicies not initialized as empty"

        assert type(init_runinfo.average_indicies) is tuple, "runinfo.average_indicies not initialized as tuple"
        assert len(init_runinfo.average_indicies) == 0, "runinfo.average_indicies not initialized as empty"

        with pytest.raises(IndexError):
            init_runinfo.average_index, "tuple index out of range when trying to call average_index"

        assert init_runinfo.has_average_scan is False, "runinfo registered as having average scan on initialization."

        # now testing legacy nomenclature
        assert init_runinfo.loop0 == init_runinfo.scan0, "loop0 did not return scan0. Not backward compatible."
        assert init_runinfo.loop1 == init_runinfo.scan1, "loop1 did not return scan1. Not backward compatible."
        assert init_runinfo.loop2 == init_runinfo.scan2, "loop2 did not return scan2. Not backward compatible."
        assert init_runinfo.loop3 == init_runinfo.scan3, "loop3 did not return scan3. Not backward compatible."

        assert init_runinfo.loops == init_runinfo.scans, "loops did not return scans. Not backward compatible."

        # testing function included at the end of runinfo.py, but not in runinfo as a method
        assert drop([0, 1, 2, 3], 2) == [0, 1, 3]

    check_runinfo_at_properties()
