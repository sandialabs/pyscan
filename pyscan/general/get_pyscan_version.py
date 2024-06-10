import os
import json


# function that gets the overarching version of pyscan from VERSION.json
def get_pyscan_version(path="../../VERSION.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, path)
    with open(path) as version_file:
        version = json.load(version_file)['version']
        if type(version) is str:
            return 'v' + version
        else:
            return "no valid version found"
