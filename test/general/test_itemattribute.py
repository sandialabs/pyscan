import pyscan as ps


def test_ItemAttribute():

    ia = ps.ItemAttribute()

    ia.test_prop1 = 3
    ia.test_prop2 = 'str'

    assert ia.test_prop1 == 3
    assert ia['test_prop1'] == 3
    assert ia.test_prop2 == 'str'
    assert ia['test_prop2'] == 'str'

    assert list(ia.keys()) == (['test_prop1', 'test_prop2'])
    assert list(ia.values()) == [3, 'str']
    assert list(ia.items()) == [('test_prop1', 3), ('test_prop2', 'str')]

    assert hasattr(ia, 'test_prop1')
    assert hasattr(ia, 'test_prop2')

    del ia.test_prop1
    assert not hasattr(ia, 'test_prop1')
