def test_sum():
    assert sum([1,1]) == 2, "Should be 2"
    
def test_len_vs__len__():
    a_tuple = (1,2,3,5)
    assert len(a_tuple) == a_tuple.__len__(), "Function len returned differnt result than method __len__"
    
if __name__ == "__main__":
    test_sum()
    test_len_vs__len__()
    print('All tests passed.')
