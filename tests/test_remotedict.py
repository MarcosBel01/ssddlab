import pytest
from remotetypes.remotedict import RemoteDict
import RemoteTypes as rt  # Importar excepciones personalizadas

def test_remove_existing_key():
    rdict = RemoteDict()
    rdict.setItem('key1', 'value1')
    rdict.remove('key1')
    assert not rdict.contains('key1')

def test_remove_nonexistent_key():
    rdict = RemoteDict()
    with pytest.raises(rt.KeyError):
        rdict.remove('nonexistent_key')

def test_length():
    rdict = RemoteDict()
    assert rdict.length() == 0
    rdict.setItem('key1', 'value1')
    assert rdict.length() == 1
    rdict.setItem('key2', 'value2')
    assert rdict.length() == 2


def test_contains():
    rdict = RemoteDict()
    assert not rdict.contains('key1')
    rdict.setItem('key1', 'value1')
    assert rdict.contains('key1')

def test_hash():
    rdict = RemoteDict()
    initial_hash = rdict.hash()
    rdict.setItem('key1', 'value1')
    new_hash = rdict.hash()
    assert initial_hash != new_hash
    rdict.remove('key1')
    assert rdict.hash() == initial_hash

def test_setItem():
    rdict = RemoteDict()
    rdict.setItem('key1', 'value1')
    assert rdict.getItem('key1') == 'value1'

def test_getItem_existing_key():
    rdict = RemoteDict()
    rdict.setItem('key1', 'value1')
    assert rdict.getItem('key1') == 'value1'

def test_getItem_nonexistent_key():
    rdict = RemoteDict()
    with pytest.raises(rt.KeyError):
        rdict.getItem('key2')

def test_pop_existing_key():
    rdict = RemoteDict()
    rdict.setItem('key1', 'value1')
    value = rdict.pop('key1')
    assert value == 'value1'
    assert not rdict.contains('key1')

def test_pop_nonexistent_key():
    rdict = RemoteDict()
    with pytest.raises(rt.KeyError):
        rdict.pop('key2')
