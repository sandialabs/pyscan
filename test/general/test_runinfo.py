'''
Pytest functions to test the Runinfo class
'''
import pyscan as ps
import sys

sys.path.append('../../../pyscan')


def test_init_from_noparams():
    """
    Testing init from no paramaters in RunInfo

    Returns
    -------
    None

    """

    init_runinfo = ps.RunInfo()

    # check that runinfo loops are initialized correctly
    def checkOne():
        # assert not hasattr(init_runinfo.loop0, 'scan_dict')
        assert init_runinfo.loop0.scan_dict == {}, "runinfo loop0 (Property Scan) scan_dict not empty when intialized"
        assert init_runinfo.loop1.scan_dict == {}, "runinfo loop1 (Property Scan) scan_dict not empty when intialized"
        assert init_runinfo.loop2.scan_dict == {}, "runinfo loop2 (Property Scan) scan_dict not empty when intialized"
        assert init_runinfo.loop3.scan_dict == {}, "runinfo loop3 (Property Scan) scan_dict not empty when intialized"
        assert init_runinfo.loop0.prop is None, "runinfo loop0 (Property Scan) prop not None when intialized"
        assert init_runinfo.loop1.prop is None, "runinfo loop1 (Property Scan) prop not None when intialized"
        assert init_runinfo.loop2.prop is None, "runinfo loop2 (Property Scan) prop not None when intialized"
        assert init_runinfo.loop3.prop is None, "runinfo loop3 (Property Scan) prop not None when intialized"
        assert init_runinfo.loop0.dt == 0, "runinfo loop0 (Property Scan) prop not 0 when intialized"
        assert init_runinfo.loop1.dt == 0, "runinfo loop1 (Property Scan) prop not 0 when intialized"
        assert init_runinfo.loop2.dt == 0, "runinfo loop2 (Property Scan) prop not 0 when intialized"
        assert init_runinfo.loop3.dt == 0, "runinfo loop3 (Property Scan) prop not 0 when intialized"
        assert init_runinfo.loop0.i == 0, "runinfo loop3 (Property Scan) i not 0 when intialized"
        assert init_runinfo.loop1.i == 0, "runinfo loop3 (Property Scan) i not 0 when intialized"
        assert init_runinfo.loop2.i == 0, "runinfo loop3 (Property Scan) i not 0 when intialized"
        assert init_runinfo.loop3.i == 0, "runinfo loop3 (Property Scan) i not 0 when intialized"

    checkOne()

    # check that runinfo static and measured are initialized correctly
    def checkTwo():
        assert not init_runinfo.static, "runinfo static not empty when intialized"
        assert not init_runinfo.measured, "runinfo measured not empty when intialized"
        
    checkTwo()

    # check that runinfo measure and trigger functions are initialized correctly
    def checkThree():
        assert not init_runinfo.measure_function, "runinfo measure_function not None when intialized"
        assert not init_runinfo.trigger_function, "runinfo trigger_function not None when intialized"

    checkThree()

    # check that runinfo initial pause, average d, and verbose settings are initialized correctly
    def checkFour():
        assert init_runinfo.initial_pause == 0.1, "runinfo initial_pause not 0.1 when intialized"
        assert init_runinfo.average_d == -1, "runinfo average_d not -1 when intialized"
        assert not init_runinfo.verbose, "runinfo verbose not set to False when intialized"

    checkFour()
