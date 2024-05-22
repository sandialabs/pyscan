import os
import json


# The dict keys are a unique pyvisa ID listed when querying the resource manager and
# the values are file names for the driver version json files kept in the driver_versions.
driver_dict = {
    'SR830': 'stanford830',
    'Keithley Instruments Inc.,Model 2260B': 'keithley2260B'
    }


def get_version(path="../../VERSION.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, path)
    with open(path) as version_file:
        version = json.load(version_file)['version']
        if type(version) is str:
            return 'v' + version
        else:
            return "no valid version found"


def get_date_tested(path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, path)
    with open(path) as version_file:
        date_tested = json.load(version_file)['date']
        if type(date_tested) is str:
            return date_tested
        else:
            return "no valid date found"


def get_driver_version_file_name(instrument_id):
    file_name = None

    for key in driver_dict.keys():
        if key in instrument_id:
            file_name = driver_dict[key]

    return file_name


def get_driver_version(instrument_id):
    file_name = get_driver_version_file_name(instrument_id)

    if file_name is None:
        return "version not found"
    else:
        path = '../drivers/driver_versions/{}.json'.format(file_name)
        version = get_version(path)
        date_tested = get_date_tested(path)
        return version, date_tested
