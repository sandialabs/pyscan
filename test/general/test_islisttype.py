import pyscan as ps
import numpy as np


def test_is_list_type():

    list1 = (1, 2, 3)
    list2 = [1, 2, 3]
    list3 = np.array([1, 2, 3])
    
    notlist1 = 'string'
    notlist2 = 2
    
    assert ps.is_list_type(list1)
    assert ps.is_list_type(list2)
    assert ps.is_list_type(list3)

    assert not ps.is_list_type(notlist1)
    assert not ps.is_list_type(notlist2)
