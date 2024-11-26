# client.py

import sys
import Ice
import RemoteTypes as rt

def main():
    with Ice.initialize(sys.argv) as communicator:
        # Configurar el proxy de la fábrica
        factory_proxy = communicator.stringToProxy("Factory:tcp -h localhost -p 10000")
        factory = rt.FactoryPrx.checkedCast(factory_proxy)
        if not factory:
            print('Invalid factory proxy')
            return 1

        # Obtener un RemoteList
        rlist_prx = factory.get(rt.TypeName.RList, 'my_list')
        rlist = rt.RListPrx.checkedCast(rlist_prx)

        # Usar RemoteList
        rlist.append('Hello')
        rlist.append('World')
        print(f'List length: {rlist.length()}')
        print(f'Item at index 0: {rlist.getItem(0)}')

        # Obtener un iterador
        iterator = rlist.iter()
        try:
            while True:
                item = iterator.next()
                print(f'Iterated item: {item}')
        except rt.StopIteration:
            pass
        except rt.CancelIteration:
            print('Iterator was invalidated')


        rdict_prx = factory.get(rt.TypeName.RDict, 'my_dict')
        rdict = rt.RDictPrx.checkedCast(rdict_prx)

        rdict.setItem('key1', 'value1')
        rdict.setItem('key2', 'value2')
        print(f'Dict length: {rdict.length()}')
        print(f'Value for key1: {rdict.getItem("key1")}')
        print(f'Value for key2: {rdict.getItem("key2")}')

        dict_iterator = rdict.iter()
        try:
            while True:
                key = dict_iterator.next()
                print(f'Iterated key: {key}')
        except rt.StopIteration:
            pass
        except rt.CancelIteration:
            print('Iterator was invalidated')
        # Obtener un RemoteSet
        rset_prx = factory.get(rt.TypeName.RSet, 'my_set')
        rset = rt.RSetPrx.checkedCast(rset_prx)

# Usar RemoteSet
        rset.add('item1')
        rset.add('item2')
        print(f'Set length: {rset.length()}')
        print(f'Contains item1: {rset.contains("item1")}')
        print(f'Contains item3: {rset.contains("item3")}')

# Obtener un iterador
        set_iterator = rset.iter()
        try:
            while True:
                item = set_iterator.next()
                print(f'Iterated item: {item}')
        except rt.StopIteration:
            pass
        except rt.CancelIteration:
            print('Iterator was invalidated')
    return 0

if __name__ == '__main__':
    sys.exit(main())
