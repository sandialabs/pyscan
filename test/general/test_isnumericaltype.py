import pyscan as ps
import numpy as np


def test_is_numeric_type():

    num1 = 2
    num2 = 2.1

    notnum1 = 'string'
    notnum2 = (1, 2, 3)
    notnum3 = [1, 2, 3]
    notnum4 = np.array([1, 2, 3])

    assert ps.is_numeric_type(num1)
    assert ps.is_numeric_type(num2)

    assert not ps.is_numeric_type(notnum1)
    assert not ps.is_numeric_type(notnum2)
    assert not ps.is_numeric_type(notnum3)
    assert not ps.is_numeric_type(notnum4)
