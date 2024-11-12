import pytest
import pyscan as ps


@pytest.fixture(scope='session')
def devices():
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    devices.v3 = ps.TestVoltage()
    devices.v4 = ps.TestVoltage()
    return devices


def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = expt.runinfo.scan0.i
    d.x2 = [d.x1 for _ in range(2)]
    d.x3 = [[expt.runinfo.scan0.i, expt.runinfo.scan0.i] for _ in range(2)]

    return d


@pytest.fixture(scope='session')
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_up_to_3D
    runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage', dt=0)
    return runinfo


def test_save_metadata(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.check_runinfo()
    expt.save_metadata()
    # now check that metadata was saved


def test_preallocate(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.check_runinfo()
    data = expt.runinfo.measure_function(expt)
    expt.preallocate(data) # what needs tob e asserted here?
    # now check that data was preallocated was saved


def test_save_point(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.check_runinfo()
    data = expt.runinfo.measure_function(expt)
    expt.preallocate(data)
    expt.save_point(data)
    # now test that single point was saved correctly
