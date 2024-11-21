import pyscan as ps
import pytest


@pytest.mark.parametrize("input,output", [
    (('a', 'b'), 'a'),
    ('a', 'a')])
def test_first_string(input, output):
    assert ps.first_string(input) == output, f"First string of {input} incorrection output {output}"


@pytest.mark.parametrize("input", [
    0,
    True,
    [0, 1],
    [0, 'b']])
def test_first_string_error(input):
    with pytest.raises(TypeError):
        ps.first_string(input)
