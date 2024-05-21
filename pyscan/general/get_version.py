import os
import json


def get_version(path="../../VERSION.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, path)
    with open(path) as version_file:
        version = json.load(version_file)['version']
        if type(version) is str:
            return 'v' + version
        else:
            return "no valid version found"


def get_driver_version(instrument_id):
    driver_dict = {'SR830': 'stanford830'}
    file_name = None

    for key in driver_dict.keys():
        if key in instrument_id:
            file_name = driver_dict[key]

    if file_name is None:
        return "version not found"
    else:
        path = '../drivers/driver_versions/{}.json'.format(file_name)
        return get_version(path)
