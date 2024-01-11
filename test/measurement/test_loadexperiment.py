'''
Pytest functions to test the load experiment function
'''

import pyscan as ps
import pytest
import os
from pathlib import Path

# This will need to be changed to omit the \..\.. but is in place for my current testing system
ROOT_DIR = os.path.abspath(os.curdir) + r'\..\..'
#ROOT_DIR = os.path.abspath(os.curdir)


def test_load_experiment():
    """
    Testing load experiment function

    Returns
    --------
    None
    """

    # for testing different files to see if they load or not. Must use actual experiment files to pass.
    def test_different_files(file_name):
        file_path = Path(file_name)
        if '.pk1' in file_name or '.hdf5' in file_name or file_path.with_suffix('.pkl').is_file() or file_path.with_suffix('.hdf5').is_file():
            expt = ps.load_experiment(file_name)
        else:
            with pytest.raises(Exception):
                ps.load_experiment(file_name)
        
        assert hasattr(expt, 'runinfo'), "loaded experiment does not have runinfo attribute"
        assert hasattr(expt, 'devices'), "loaded experiment does not have devices attribute"

        assert isinstance(expt, ps.ItemAttribute), "expt is not an instance of item attribute"
        assert isinstance(expt.runinfo, ps.ItemAttribute), "expt is not an instance of item attribute"
        assert isinstance(expt.devices, ps.ItemAttribute), "expt is not an instance of item attribute"
        
        print(expt.runinfo.__dict__)

    file_name = ROOT_DIR + r'\demo_notebooks\backup\20231129T090758.hdf5'
    test_different_files(file_name)


test_load_experiment()
