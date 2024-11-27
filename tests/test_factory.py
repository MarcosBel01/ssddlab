# test_factory.py
import pytest
import RemoteTypes as rt  # Importar excepciones y tipos
from remotetypes.factory import Factory

def test_factory_get_rdict(ice_adapter):
    factory = Factory(ice_adapter)
    factory_proxy = ice_adapter.addWithUUID(factory)
    factory_prx = rt.FactoryPrx.checkedCast(factory_proxy)
    rdict_prx = factory_prx.get(rt.TypeName.RDict)
    assert isinstance(rdict_prx, rt.RDictPrx)
    # Usar el RDict obtenido
    rdict_prx.setItem('key1', 'value1')
    assert rdict_prx.getItem('key1') == 'value1'

def test_factory_get_rlist(ice_adapter):
    factory = Factory(ice_adapter)
    factory_proxy = ice_adapter.addWithUUID(factory)
    factory_prx = rt.FactoryPrx.checkedCast(factory_proxy)
    rlist_prx = factory_prx.get(rt.TypeName.RList)
    assert isinstance(rlist_prx, rt.RListPrx)
    # Usar el RList obtenido
    rlist_prx.append('item1')
    assert rlist_prx.getItem(0) == 'item1'

def test_factory_get_rset(ice_adapter):
    factory = Factory(ice_adapter)
    factory_proxy = ice_adapter.addWithUUID(factory)
    factory_prx = rt.FactoryPrx.checkedCast(factory_proxy)
    rset_prx = factory_prx.get(rt.TypeName.RSet)
    assert isinstance(rset_prx, rt.RSetPrx)
    # Usar el RSet obtenido
    rset_prx.add('item1')
    assert rset_prx.contains('item1')

def test_factory_get_existing_rdict(ice_adapter):
    factory = Factory(ice_adapter)
    factory_proxy = ice_adapter.addWithUUID(factory)
    factory_prx = rt.FactoryPrx.checkedCast(factory_proxy)
    rdict1_prx = factory_prx.get(rt.TypeName.RDict, 'test_dict')
    rdict1_prx.setItem('key1', 'value1')

    rdict2_prx = factory_prx.get(rt.TypeName.RDict, 'test_dict')
    assert rdict2_prx.getItem('key1') == 'value1'

def test_factory_get_existing_rlist(ice_adapter):
    factory = Factory(ice_adapter)
    factory_proxy = ice_adapter.addWithUUID(factory)
    factory_prx = rt.FactoryPrx.checkedCast(factory_proxy)
    rlist1_prx = factory_prx.get(rt.TypeName.RList, 'test_list')
    rlist1_prx.append('item1')

    rlist2_prx = factory_prx.get(rt.TypeName.RList, 'test_list')
    assert rlist2_prx.getItem(0) == 'item1'

def test_factory_get_existing_rset(ice_adapter):
    factory = Factory(ice_adapter)
    factory_proxy = ice_adapter.addWithUUID(factory)
    factory_prx = rt.FactoryPrx.checkedCast(factory_proxy)
    rset1_prx = factory_prx.get(rt.TypeName.RSet, 'test_set')
    rset1_prx.add('item1')

    rset2_prx = factory_prx.get(rt.TypeName.RSet, 'test_set')
    assert rset2_prx.contains('item1')
