from pyscan.general.get_pyscan_version import get_pyscan_version


def test_get_version():
    version = get_pyscan_version()
    assert type(version) is str, "get_version did not return a string"
    assert version != "no valid version found", "get_version did not find the version file"
    assert version[0] == 'v', "version string did not start with v"
