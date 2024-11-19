import pyscan as ps
import numpy as np
import pytest


@pytest.fixture()
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_up_to_3D
    return runinfo


@pytest.fixture()
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


## Test RepeatScan
@pytest.fixture
def repeat_scan():
    return ps.RepeatScan(2)


@pytest.mark.parametrize('key,value', [
    ('scan_dict', {'repeat': np.array([0, 1])}),
    ('device_names', ['repeat']),
    ('dt', 0),
    ('i', 0),
    ('n', 2)
])
def test_repeat_scan_init(repeat_scan, key, value):
    if key == 'scan_dict':
        for key1, value1 in value.items():
            assert np.all(repeat_scan.scan_dict[key1] == value[key1]), f"Property scan attribute {key} != {value}"
    else:
        assert repeat_scan[key] == value, f"Property scan attribute {key} != {value}"


def test_repeat_scan_iterate_m1(runinfo, devices, repeat_scan):
    runinfo.scan0 = repeat_scan
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 0, -1)
    assert expt.runinfo.scan0.i == 0


def test_repeat_scan_no_iterate(runinfo, devices, repeat_scan):
    runinfo.scan0 = repeat_scan
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 0, 0)
    assert expt.runinfo.scan0.i == 0


def test_repeat_scan_iterate_one(runinfo, devices, repeat_scan):
    runinfo.scan0 = repeat_scan
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 1, 1)
    assert expt.runinfo.scan0.i == 1
