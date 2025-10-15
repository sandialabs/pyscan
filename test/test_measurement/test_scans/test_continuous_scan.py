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
    return devices


def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = expt.runinfo.scan0.i
    d.x2 = [d.x1 for _ in range(2)]
    d.x3 = [[expt.runinfo.scan0.i, expt.runinfo.scan0.i] for _ in range(2)]

    return d


@pytest.mark.parametrize('key,value', [
    ('scan_dict', {'iteration': np.array([])}),
    ('device_names', ['iteration']),
    ('dt', 0),
    ('i', 0),
    ('n', 1),
    ('n_max', 10)
])
def test_continuous_scan_init(key, value):
    continuous_scan = ps.ContinuousScan(n_max=10)
    if key == 'scan_dict':
        for key1, value1 in value.items():
            assert np.all(continuous_scan.scan_dict[key1] == value[key1]), f"Continuous scan attribute {key} != {value}"
    else:
        assert continuous_scan[key] == value, f"Continuous scan attribute {key} != {value}"


def test_continuous_scan_iterate_m1(runinfo, devices):
    runinfo.scan0 = ps.ContinuousScan(n_max=10)
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 0, -1)
    assert expt.runinfo.scan0.i == 0
    assert expt.runinfo.scan0.n == 1


def test_continuous_scan_no_iterate(runinfo, devices):
    runinfo.scan0 = ps.ContinuousScan(n_max=10)
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 0, 0)
    assert expt.runinfo.scan0.i == 0
    assert expt.runinfo.scan0.n == 1


def test_continuous_scan_iterate_one(runinfo, devices):
    runinfo.scan0 = ps.ContinuousScan(n_max=10)
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 1, 1)
    assert expt.runinfo.scan0.i == 1
    assert expt.runinfo.scan0.n == 2
