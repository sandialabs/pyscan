import pyscan as ps
import numpy as np


def test_drange():
    
    # If the start and end value are the same, give a single valued array
    values = ps.drange(1, 0.01, 1)
    assert values == [1], "drange(1, 0.01, 1) gave wrong output"

    values = ps.drange(1, 0.01, 1.005)
    assert values == [1, 1.005], "drange(1, 0.01, 1.005) gave wrong output"

    values = ps.drange(1, 0.01, 1.2)
    works = np.all(np.round(np.arange(1, 1.21, 0.01), 5)
                   == np.round(values, 5))
    assert works, "ps.drange(1, 0.01, 1.2) gave wrong output"

    values = ps.drange(1, 0.015, 1.2)
    test_values = np.append(np.round(np.arange(1, 1.195, 0.015), 5), 1.2) 
    assert np.all(values == test_values), "ps.drange(1, 0.015, 1.2) gave wrong output"

    # Negative direcions
    values = ps.drange(1.005, 0.01, 1)
    assert values == [1.005, 1], "ps.drange(1.005, 0.01, 1) failed"

    values = ps.drange(1.2, 0.01, 1)
    works = np.all(np.round(np.arange(1.20, 0.99, -0.01), 5)
                   == np.round(values, 5))
    assert works, "ps.drange(1.2, 0.01, 1) gave wrong output"

    values = np.round(ps.drange(1.2, 0.015, 1), 5)
    test_values = np.round(np.append(np.arange(1.2, 1.005, -0.015), 1), 5)
    assert np.all(values == test_values), "ps.drange(1.2, 0.015, 1) gave the wrong output"
