import pytest
from remotetypes.remoteset import RemoteSet
import RemoteTypes as rt  

def test_remove_existing_item():
    rset = RemoteSet()
    rset.add('item1')
    rset.remove('item1')
    assert not rset.contains('item1')

def test_remove_nonexistent_item():
    rset = RemoteSet()
    with pytest.raises(rt.KeyError):
        rset.remove('item2')

def test_length():
    rset = RemoteSet()
    assert rset.length() == 0
    rset.add('item1')
    assert rset.length() == 1
    rset.add('item2')
    assert rset.length() == 2

def test_contains():
    rset = RemoteSet()
    assert not rset.contains('item1')
    rset.add('item1')
    assert rset.contains('item1')

def test_hash():
    rset = RemoteSet()
    initial_hash = rset.hash()
    rset.add('item1')
    new_hash = rset.hash()
    assert initial_hash != new_hash
    rset.remove('item1')
    assert rset.hash() == initial_hash

def test_add_new_item():
    rset = RemoteSet()
    rset.add('item1')
    assert rset.length() == 1

def test_add_existing_item():
    rset = RemoteSet()
    rset.add('item1')
    rset.add('item1')  
    assert rset.length() == 1

def test_pop():
    rset = RemoteSet()
    rset.add('item1')
    rset.add('item2')
    item = rset.pop()
    assert item in ['item1', 'item2']
    assert rset.length() == 1

def test_pop_until_empty():
    rset = RemoteSet()
    rset.add('item1')
    rset.pop()
    with pytest.raises(rt.KeyError):
        rset.pop()

def test_pop_empty_set():
    rset = RemoteSet()
    with pytest.raises(rt.KeyError):
        rset.pop()
