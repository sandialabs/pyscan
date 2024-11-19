import pytest
import pyscan as ps
import os
import h5py
import json
import numpy as np


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


@pytest.fixture()
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_up_to_3D
    runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage', dt=0)
    return runinfo


@pytest.mark.parametrize("data_dir", [None, './test'])
def test_setup_data_directory(runinfo, devices, data_dir):
    expt = ps.Experiment(runinfo, devices, data_dir=data_dir)
    if data_dir is None:
        assert os.path.isdir('./backup'), "Data Directory not correctly setup"
    else:
        assert os.path.isdir(data_dir), "Data Directory not correctly setup"


def test_check_runinfo(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.check_runinfo()
    assert hasattr(expt.runinfo, 'file_name')


def test_save_runinfo_metadata(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.check_runinfo()
    expt.save_metadata('runinfo')

    with h5py.File('./backup/{}'.format(expt.runinfo.file_name + '.hdf5'), 'r') as f:
        runinfo = f.attrs['runinfo']

    runinfo = json.loads(runinfo)

    # expected = {
    #     'measured': [],
    #     'measure_function': 'def measure_up_to_3D(expt):\n    d = ps.ItemAttribute()\n\n    d.x1 = expt.runinfo.scan0.i\n    d.x2 = [d.x1 for _ in range(2)]\n    d.x3 = [[expt.runinfo.scan0.i, expt.runinfo.scan0.i] for _ in range(2)]\n\n    return d\n',
    #     'initial_pause': 0.1,
    #     '_pyscan_version': ps.get_pyscan_version(),
    #     'scan0': {
    #         'prop': 'voltage',
    #         'scan_dict': {'v1_voltage': [0.0, 0.1]},
    #         'device_names': ['v1'],
    #         'dt': 0,
    #         'i': 0,
    #         'n': 2},
    #     'data_path': 'backup',
    #     'file_name':  expt.runinfo.file_name,
    #     'average_d': -1,
    #     'continuous': False}

    # for key in runinfo.keys():
    #     assert runinfo[key] == expected[key]


def test_save_devices_metadata(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.check_runinfo()
    expt.save_metadata('devices')

    with h5py.File('./backup/{}'.format(expt.runinfo.file_name + '.hdf5'), 'r') as f:
        devices = f.attrs['devices']

    devices = json.loads(devices)

    expected = {
        'v1': {
            'instrument': None,
            '_driver_class': 'NoneType',
            'debug': False,
            '_instrument_driver_version': '0.2.0',
            '_voltage_settings': {
                'name': 'voltage',
                'write_string': 'VOLT {}',
                'query_string': 'VOLT?',
                'range': [-10, 10],
                'return_type': 'float'},
            '_power_settings': {
                'name': 'power',
                'write_string': 'POW {}',
                'query_string': 'POW?',
                'values': [1, 10],
                'return_type': 'int'},
            '_output_state_settings': {
                'name': 'output_state',
                'write_string': 'OUTP {}',
                'query_string': 'OUTP?',
                'dict_values': {'on': 1, 'off': 0, '1': 1, '0': 0},
                'return_type': 'str'},
            '_voltage': 0.0,
            '_power': 1,
            '_output_state': 'off',
            '_version': '0.1.0',
            'black_list_for_testing': []}}

    for key in devices.keys():
        assert devices[key] == expected[key]


def test_preallocate(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.check_runinfo()
    data = expt.runinfo.measure_function(expt)
    expt.preallocate(data)

    assert expt.runinfo.measured == ['x1', 'x2', 'x3']

    assert expt.x1.shape == (2,)
    assert np.all(np.isnan(expt.x1))

    assert expt.x2.shape == (2, 2)
    assert np.all(np.isnan(expt.x2))

    assert expt.x3.shape == (2, 2, 2)
    assert np.all(np.isnan(expt.x3))

    with h5py.File('./backup/{}'.format(expt.runinfo.file_name + '.hdf5'), 'r') as f:
        scan = f['v1_voltage']
        assert scan.shape == (2,)
        assert np.allclose(scan, np.array([0.0, 0.1]))

        x1 = f['x1']
        assert x1.shape == (2,)
        assert np.all(np.isnan(x1))
        x2 = f['x2']
        assert x2.shape == (2, 2)
        assert np.all(np.isnan(x2))

        x3 = f['x3']
        assert x3.shape == (2, 2, 2)
        assert np.all(np.isnan(x3))


def test_save_point(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.check_runinfo()
    data = expt.runinfo.measure_function(expt)
    expt.preallocate(data)
    expt.save_point(data)

    assert expt.x1.shape == (2,)
    assert np.isclose(expt.x1[0], 0.0)
    assert np.isnan(expt.x1[1])

    assert expt.x2.shape == (2, 2)
    assert np.allclose(expt.x2[0], [0, 0])
    assert np.all(np.isnan(expt.x2[1]))

    assert expt.x3.shape == (2, 2, 2)
    assert np.allclose(expt.x3[0], np.zeros((2, 2)))
    assert np.all(np.isnan(expt.x3[1]))

    with h5py.File('./backup/{}'.format(expt.runinfo.file_name + '.hdf5'), 'r') as f:
        scan = f['v1_voltage']
        assert scan.shape == (2,)
        assert np.allclose(scan, np.array([0.0, 0.1]))

        x1 = f['x1']
        assert x1.shape == (2,)
        assert np.isclose(x1[0], [0.0])
        print(np.array(x1))
        assert np.all(np.isnan(x1[1]))

        x2 = f['x2']
        assert x2.shape == (2, 2)
        assert np.allclose(x2[0], [0, 0])
        assert np.all(np.isnan(x2[1]))

        x3 = f['x3']
        assert x3.shape == (2, 2, 2)
        assert np.allclose(x3[0], np.zeros((2, 2)))
        assert np.all(np.isnan(x3[1]))
