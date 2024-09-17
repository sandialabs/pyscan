import pyscan as ps
import pytest


def test_legacy():
    '''
    Ensure that legacy naming convention fails.
    '''
    devices = ps.ItemAttribute()
    runinfo = ps.RunInfo()
    with pytest.raises(Exception):
        runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    with pytest.raises(Exception):
        runinfo.loop1 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    with pytest.raises(Exception):
        runinfo.loop2 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    with pytest.raises(Exception):
        runinfo.loop3 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    with pytest.raises(Exception):
        sweep = ps.Sweep(runinfo, devices)
        assert isinstance(sweep, ps.Experiment)
    with pytest.raises(Exception):
        metasweep = ps.MetaSweep(runinfo, devices, None)
        assert isinstance(metasweep, ps.AbstractExperiment)
