import pyscan as ps
import numpy as np
import pytest


@pytest.mark.parametrize("input", [2, 2.1, np.float64(2)])
def test_is_numeric_type(input):
    assert ps.is_numeric_type(input)


@pytest.mark.parametrize("input", [
    'string',
    (1, 2, 3),
    [1, 2, 3],
    np.array([1, 2, 3]),
    {'a': 1},
    True])
def test_is_not_numeric_type(input):
    assert not ps.is_numeric_type(input), f"{input} was wrongly identified as numeric type"
