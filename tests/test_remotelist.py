import pytest
from remotetypes.remotelist import RemoteList
import RemoteTypes as rt  # Importar excepciones personalizadas

def test_remove_existing_item():
    rlist = RemoteList()
    rlist.append('item1')
    rlist.remove('item1')
    assert not rlist.contains('item1')

def test_remove_nonexistent_item():
    rlist = RemoteList()
    with pytest.raises(rt.KeyError):
        rlist.remove('item2')

def test_length():
    rlist = RemoteList()
    assert rlist.length() == 0
    rlist.append('item1')
    assert rlist.length() == 1
    rlist.append('item2')
    assert rlist.length() == 2

def test_contains():
    rlist = RemoteList()
    assert not rlist.contains('item1')
    rlist.append('item1')
    assert rlist.contains('item1')

def test_hash():
    rlist = RemoteList()
    initial_hash = rlist.hash()
    rlist.append('item1')
    new_hash = rlist.hash()
    assert initial_hash != new_hash
    rlist.remove('item1')
    assert rlist.hash() == initial_hash

def test_append():
    rlist = RemoteList()
    rlist.append('item1')
    assert rlist.getItem(0) == 'item1'

def test_pop_without_index():
    rlist = RemoteList()
    rlist.append('item1')
    rlist.append('item2')
    item = rlist.pop()
    assert item == 'item2'
    assert rlist.length() == 1

def test_pop_with_index():
    rlist = RemoteList()
    rlist.append('item1')
    rlist.append('item2')
    item = rlist.pop(0)
    assert item == 'item1'
    assert rlist.length() == 1

def test_pop_invalid_index():
    rlist = RemoteList()
    with pytest.raises(rt.IndexError):
        rlist.pop(0)

def test_getItem_existing_index():
    rlist = RemoteList()
    rlist.append('item1')
    assert rlist.getItem(0) == 'item1'

def test_getItem_invalid_index():
    rlist = RemoteList()
    with pytest.raises(rt.IndexError):
        rlist.getItem(0)

def test_getItem_does_not_remove():
    rlist = RemoteList()
    rlist.append('item1')
    rlist.getItem(0)
    assert rlist.length() == 1

def test_pop_does_remove():
    rlist = RemoteList()
    rlist.append('item1')
    rlist.pop(0)
    assert rlist.length() == 0
