import pyscan as ps
import pytest 


def test_first_string():

    str1 = 'a'
    str2 = 'b'
    str_array = [str1, str2]

    assert ps.first_string(str1) == 'a'
    assert ps.first_string(str_array) == 'a'
    assert ps.first_string(str_array[::-1]) == 'b'

    with pytest.raises(TypeError):
        ps.first_string(0)
        ps.first_string([0, 1])
