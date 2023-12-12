'''
Pytest functions to test the Runinfo class
'''

import pyscan as ps


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
        # check that loops 0 - 4 initialized
        assert hasattr(init_runinfo, 'loop0'), "runinfo loop0 not intialized"
        assert hasattr(init_runinfo, 'loop1'), "runinfo loop1 not intialized"
        assert hasattr(init_runinfo, 'loop2'), "runinfo loop2 not intialized"
        assert hasattr(init_runinfo, 'loop3'), "runinfo loop3 not intialized"

        # check that loops 0 - 4 initialized
        for loop in init_runinfo.loops:
            assert isinstance(loop, ps.PropertyScan), "runinfo loops not initialized as Property Scan"

        assert hasattr(init_runinfo, 'loop0'), "runinfo loop0 not intialized"
        assert hasattr(init_runinfo, 'loop1'), "runinfo loop1 not intialized"
        assert hasattr(init_runinfo, 'loop2'), "runinfo loop2 not intialized"
        assert hasattr(init_runinfo, 'loop3'), "runinfo loop3 not intialized"

        # check that scan_dict initialized
        assert hasattr(init_runinfo.loop0, 'scan_dict'), "runinfo loop0 (Property Scan) scan_dict not intialized"
        assert hasattr(init_runinfo.loop1, 'scan_dict'), "runinfo loop1 (Property Scan) scan_dict not intialized"
        assert hasattr(init_runinfo.loop2, 'scan_dict'), "runinfo loop2 (Property Scan) scan_dict not intialized"
        assert hasattr(init_runinfo.loop3, 'scan_dict'), "runinfo loop3 (Property Scan) scan_dict not intialized"

        # check that scan_dict initialized as empty
        assert init_runinfo.loop0.scan_dict == {}, "runinfo loop0 (Property Scan) scan_dict not empty when intialized"
        assert init_runinfo.loop1.scan_dict == {}, "runinfo loop1 (Property Scan) scan_dict not empty when intialized"
        assert init_runinfo.loop2.scan_dict == {}, "runinfo loop2 (Property Scan) scan_dict not empty when intialized"
        assert init_runinfo.loop3.scan_dict == {}, "runinfo loop3 (Property Scan) scan_dict not empty when intialized"

        # check that prop initialized
        assert hasattr(init_runinfo.loop0, 'prop'), "runinfo loop0 (Property Scan) prop not intialized"
        assert hasattr(init_runinfo.loop1, 'prop'), "runinfo loop1 (Property Scan) prop not intialized"
        assert hasattr(init_runinfo.loop2, 'prop'), "runinfo loop2 (Property Scan) prop not intialized"
        assert hasattr(init_runinfo.loop3, 'prop'), "runinfo loop3 (Property Scan) prop not intialized"

        # check that prop initialized as None
        assert init_runinfo.loop0.prop is None, "runinfo loop0 (Property Scan) prop not None when intialized"
        assert init_runinfo.loop1.prop is None, "runinfo loop1 (Property Scan) prop not None when intialized"
        assert init_runinfo.loop2.prop is None, "runinfo loop2 (Property Scan) prop not None when intialized"
        assert init_runinfo.loop3.prop is None, "runinfo loop3 (Property Scan) prop not None when intialized"

        # check that dt initialized
        assert hasattr(init_runinfo.loop0, 'dt'), "runinfo loop0 (Property Scan) dt not intialized"
        assert hasattr(init_runinfo.loop1, 'dt'), "runinfo loop1 (Property Scan) dt not intialized"
        assert hasattr(init_runinfo.loop2, 'dt'), "runinfo loop2 (Property Scan) dt not intialized"
        assert hasattr(init_runinfo.loop3, 'dt'), "runinfo loop3 (Property Scan) dt not intialized"

        # check that dt initialized as 0
        assert init_runinfo.loop0.dt == 0, "runinfo loop0 (Property Scan) dt not 0 when intialized"
        assert init_runinfo.loop1.dt == 0, "runinfo loop1 (Property Scan) dt not 0 when intialized"
        assert init_runinfo.loop2.dt == 0, "runinfo loop2 (Property Scan) dt not 0 when intialized"
        assert init_runinfo.loop3.dt == 0, "runinfo loop3 (Property Scan) dt not 0 when intialized"

        # check that i initialized
        assert hasattr(init_runinfo.loop0, 'i'), "runinfo loop0 (Property Scan) i not intialized"
        assert hasattr(init_runinfo.loop1, 'i'), "runinfo loop1 (Property Scan) i not intialized"
        assert hasattr(init_runinfo.loop2, 'i'), "runinfo loop2 (Property Scan) i not intialized"
        assert hasattr(init_runinfo.loop3, 'i'), "runinfo loop3 (Property Scan) i not intialized"

        # check that i initialized as 0
        assert init_runinfo.loop0.i == 0, "runinfo loop3 (Property Scan) i not 0 when intialized"
        assert init_runinfo.loop1.i == 0, "runinfo loop3 (Property Scan) i not 0 when intialized"
        assert init_runinfo.loop2.i == 0, "runinfo loop3 (Property Scan) i not 0 when intialized"
        assert init_runinfo.loop3.i == 0, "runinfo loop3 (Property Scan) i not 0 when intialized"

    checkOne()

    # check that runinfo static and measured are initialized correctly
    def checkTwo():
        assert hasattr(init_runinfo, 'static'), "runinfo static not initialized"
        assert init_runinfo.static == {}, "runinfo static not empty when intialized"

        assert hasattr(init_runinfo, 'measured'), "runinfo measured not initialized"
        assert init_runinfo.measured == [], "runinfo measured not empty when intialized"
        
    checkTwo()

    # check that runinfo measure and trigger functions are initialized correctly
    def checkThree():
        assert hasattr(init_runinfo, 'measure_function'), "runinfo measure_function not initialized"
        assert init_runinfo.measure_function is None, "runinfo measure_function not None when intialized"

        assert hasattr(init_runinfo, 'trigger_function'), "runinfo trigger_function not initialized"
        assert init_runinfo.trigger_function is None, "runinfo trigger_function not None when intialized"

    checkThree()

    # check that runinfo initial pause, average d, and verbose settings are initialized correctly
    def checkFour():
        assert hasattr(init_runinfo, 'initial_pause'), "runinfo initial_pause not initialized"
        assert init_runinfo.initial_pause == 0.1, "runinfo initial_pause not 0.1 when intialized"
        
        assert hasattr(init_runinfo, 'average_d'), "runinfo average_d not initialized"
        assert init_runinfo.average_d == -1, "runinfo average_d not -1 when intialized"

        assert hasattr(init_runinfo, 'verbose'), "runinfo verbose not initialized"
        assert not init_runinfo.verbose, "runinfo verbose not set to False when intialized"

    checkFour()
