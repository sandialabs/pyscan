import pyscan as ps
import numpy as np
import pytest


@pytest.mark.parametrize("start, step, end, expected", [
    (1, 0.01, 1, [1]),
    (1, 0.01, 1.005, [1, 1.005]),
    (1, 0.01, 1.2, np.round(np.arange(1, 1.21, 0.01), 5)),
    (1, 0.015, 1.2, np.append(np.round(np.arange(1, 1.195, 0.015), 5), 1.2)),
    (1.005, 0.01, 1, [1.005, 1]),
    (1.2, 0.01, 1, np.round(np.arange(1.20, 0.99, -0.01), 5)),
    (1.2, 0.015, 1, np.round(np.append(np.arange(1.2, 1.005, -0.015), 1), 5))])
def test_drange_value(start, step, end, expected):
    assert np.allclose(ps.drange(start, step, end), expected), f"drange({start}, {step}, {end}) gave wrong output"
