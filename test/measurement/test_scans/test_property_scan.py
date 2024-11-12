import pyscan as ps
import numpy as np
import pytest


@pytest.fixture(scope='session')
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_up_to_3D
    return runinfo


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


## Test PropertyScan
@pytest.fixture
def property_scan():
    return ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, prop='voltage')


@pytest.mark.parametrize('key,value', [
    ('prop', 'voltage'),
    ('scan_dict', {'v1_voltage': np.array([0, 0.1])}),
    ('device_names', ['v1']),
    ('dt', 0),
    ('i', 0)
])
def test_property_scan_init(property_scan, key, value):
    if key == 'scan_dict':
        for key1, value1 in value.items():
            assert np.all(property_scan.scan_dict[key1] == value[key1]), f"Property scan attribute {key} != {value}"
    else:
        assert property_scan[key] == value, f"Property scan attribute {key} != {value}"


def test_property_scan_iterate_m1(runinfo, devices, property_scan):
    runinfo.scan0 = property_scan
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 0, -1)
    assert expt.runinfo.scan0.i == 0
    assert expt.devices.v1.voltage == 0


def test_property_scan_no_iterate(runinfo, devices, property_scan):
    runinfo.scan0 = property_scan
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 0, 0)
    assert expt.devices.v1.voltage == 0
    assert expt.runinfo.scan0.i == 0


def test_property_scan_iterate_one(runinfo, devices, property_scan):
    runinfo.scan0 = property_scan
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 1, 1)
    assert expt.devices.v1.voltage == 0.1
    assert expt.runinfo.scan0.i == 1
