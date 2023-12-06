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

    def checkOne():
        assert not init_runinfo.loop0.scan_dict
        assert not init_runinfo.loop1.scan_dict
        assert not init_runinfo.loop2.scan_dict
        assert not init_runinfo.loop3.scan_dict

    def checkTwo():
        assert not init_runinfo.static
        assert not init_runinfo.measured

    def checkThree():
        assert not init_runinfo.measure_function
        assert not init_runinfo.trigger_function

    def checkFour():
        assert init_runinfo.initial_pause == 0.1
