import os
import json


def get_version():
    runinfo_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(runinfo_dir, "../../VERSION.json")
    with open(path) as version_file:
        version = json.load(version_file)['version']
        if type(version) is str:
            return 'v' + version
        else:
            return "no valid version found"
