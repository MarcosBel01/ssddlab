# test_iterable.py
import pytest
from remotetypes.remotelist import RemoteList
from remotetypes.remotedict import RemoteDict
from remotetypes.remoteset import RemoteSet
import RemoteTypes as rt  # Importar excepciones personalizadas

def test_iterable_rlist(ice_adapter):
    # Crear el objeto RemoteList y añadir elementos
    rlist = RemoteList()
    rlist.append('item1')
    rlist.append('item2')
    # Añadir el objeto al adaptador y obtener el proxy
    proxy = ice_adapter.addWithUUID(rlist)
    rlist_prx = rt.RListPrx.checkedCast(proxy)
    # Obtener el iterador a través del proxy
    iterator_prx = rlist_prx.iter()
    # Iterar y verificar los elementos
    assert iterator_prx.next() == 'item1'
    assert iterator_prx.next() == 'item2'
    with pytest.raises(rt.StopIteration):
        iterator_prx.next()

def test_iterable_rdict(ice_adapter):
    rdict = RemoteDict()
    rdict.setItem('key1', 'value1')
    rdict.setItem('key2', 'value2')
    proxy = ice_adapter.addWithUUID(rdict)
    rdict_prx = rt.RDictPrx.checkedCast(proxy)
    iterator_prx = rdict_prx.iter()
    keys = [iterator_prx.next(), iterator_prx.next()]
    assert set(keys) == {'key1', 'key2'}
    with pytest.raises(rt.StopIteration):
        iterator_prx.next()

def test_iterable_rset(ice_adapter):
    rset = RemoteSet()
    rset.add('item1')
    rset.add('item2')
    proxy = ice_adapter.addWithUUID(rset)
    rset_prx = rt.RSetPrx.checkedCast(proxy)
    iterator_prx = rset_prx.iter()
    items = [iterator_prx.next(), iterator_prx.next()]
    assert set(items) == {'item1', 'item2'}
    with pytest.raises(rt.StopIteration):
        iterator_prx.next()

def test_iterable_invalidation_rlist(ice_adapter):
    rlist = RemoteList()
    rlist.append('item1')
    proxy = ice_adapter.addWithUUID(rlist)
    rlist_prx = rt.RListPrx.checkedCast(proxy)
    iterator_prx = rlist_prx.iter()
    # Modificar la lista a través del proxy
    rlist_prx.append('item2')
    with pytest.raises(rt.CancelIteration):
        iterator_prx.next()

def test_iterable_invalidation_rdict(ice_adapter):
    rdict = RemoteDict()
    rdict.setItem('key1', 'value1')
    proxy = ice_adapter.addWithUUID(rdict)
    rdict_prx = rt.RDictPrx.checkedCast(proxy)
    iterator_prx = rdict_prx.iter()
    # Modificar el diccionario a través del proxy
    rdict_prx.setItem('key2', 'value2')
    with pytest.raises(rt.CancelIteration):
        iterator_prx.next()

def test_iterable_invalidation_rset(ice_adapter):
    rset = RemoteSet()
    rset.add('item1')
    proxy = ice_adapter.addWithUUID(rset)
    rset_prx = rt.RSetPrx.checkedCast(proxy)
    iterator_prx = rset_prx.iter()
    # Modificar el conjunto a través del proxy
    rset_prx.add('item2')
    with pytest.raises(rt.CancelIteration):
        iterator_prx.next()
