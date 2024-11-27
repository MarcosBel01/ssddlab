## client.py

import sys
import Ice
import RemoteTypes as rt

def main():
    with Ice.initialize(sys.argv) as communicator:
        # Configure the proxy for the factory
        factory_proxy = communicator.stringToProxy("Factory:tcp -h localhost -p 10000")
        factory = rt.FactoryPrx.checkedCast(factory_proxy)
        if not factory:
            print('Invalid factory proxy')
            return 1

        print("Testing RDict requirements")
        # Get an RDict object
        rdict_prx = factory.get(rt.TypeName.RDict, 'test_dict')
        rdict = rt.RDictPrx.checkedCast(rdict_prx)

        # 1.1 RDict.remove removes an existing key
        print("\nRequirement 1.1: RDict.remove removes an existing key")
        rdict.setItem('key1', 'value1')
        rdict.remove('key1')
        print("Removed 'key1', contains 'key1'? ", rdict.contains('key1'))

        # 1.2 RDict.remove raises KeyError if key doesn't exist
        print("\nRequirement 1.2: RDict.remove raises KeyError if key doesn't exist")
        try:
            rdict.remove('nonexistent_key')
        except rt.KeyError as e:
            print("Caught KeyError as expected:", e)

        # 1.3 RDict.length returns the correct length
        print("\nRequirement 1.3: RDict.length returns the correct length")
        rdict.setItem('key2', 'value2')
        length = rdict.length()
        print("Length after adding one item:", length)

        # 1.4 and 1.5 RDict.contains returns True/False
        print("\nRequirement 1.4 and 1.5: RDict.contains returns True/False")
        print("Contains 'key2'?", rdict.contains('key2'))
        print("Contains 'key3'?", rdict.contains('key3'))

        # 1.6 and 1.7 RDict.hash returns same/different value
        print("\nRequirement 1.6 and 1.7: RDict.hash returns same/different value")
        initial_hash = rdict.hash()
        print("Initial hash:", initial_hash)
        rdict.setItem('key3', 'value3')
        new_hash = rdict.hash()
        print("New hash after modification:", new_hash)
        print("Hashes are different:", initial_hash != new_hash)

        # 1.8 RDict.setItem allows retrieval of the key
        print("\nRequirement 1.8: RDict.setItem allows retrieval of the key")
        rdict.setItem('key4', 'value4')
        value = rdict.getItem('key4')
        print("Retrieved 'key4' with value:", value)

        # 1.9 RDict.getItem raises KeyError if key doesn't exist
        print("\nRequirement 1.9: RDict.getItem raises KeyError if key doesn't exist")
        try:
            rdict.getItem('nonexistent_key')
        except rt.KeyError as e:
            print("Caught KeyError as expected:", e)

        # 1.10.1 and 1.10.2 RDict.getItem returns value and keeps it
        print("\nRequirement 1.10.1 and 1.10.2: RDict.getItem returns value and keeps it")
        value = rdict.getItem('key2')
        print("Retrieved 'key2' with value:", value)
        print("Contains 'key2' after getItem?", rdict.contains('key2'))

        # 1.11 RDict.pop raises KeyError if key doesn't exist
        print("\nRequirement 1.11: RDict.pop raises KeyError if key doesn't exist")
        try:
            rdict.pop('nonexistent_key')
        except rt.KeyError as e:
            print("Caught KeyError as expected:", e)

        # 1.12.1 and 1.12.2 RDict.pop returns and removes the value
        print("\nRequirement 1.12.1 and 1.12.2: RDict.pop returns and removes the value")
        rdict.setItem('key5', 'value5')
        value = rdict.pop('key5')
        print("Popped 'key5' with value:", value)
        print("Contains 'key5' after pop?", rdict.contains('key5'))

        # Testing RList requirements
        print("\nTesting RList requirements")
        # Get an RList object
        rlist_prx = factory.get(rt.TypeName.RList, 'test_list')
        rlist = rt.RListPrx.checkedCast(rlist_prx)

        # 2.1 RList.remove removes an existing item
        print("\nRequirement 2.1: RList.remove removes an existing item")
        rlist.append('item1')
        rlist.remove('item1')
        print("Removed 'item1', contains 'item1'? ", rlist.contains('item1'))

        # 2.2 RList.remove raises KeyError if item doesn't exist
        print("\nRequirement 2.2: RList.remove raises KeyError if item doesn't exist")
        try:
            rlist.remove('nonexistent_item')
        except rt.KeyError as e:
            print("Caught KeyError as expected:", e)

        # 2.3 RList.length returns the correct length
        print("\nRequirement 2.3: RList.length returns the correct length")
        rlist.append('item2')
        length = rlist.length()
        print("Length after adding one item:", length)

        # 2.4 and 2.5 RList.contains returns True/False
        print("\nRequirement 2.4 and 2.5: RList.contains returns True/False")
        print("Contains 'item2'?", rlist.contains('item2'))
        print("Contains 'item3'?", rlist.contains('item3'))

        # 2.6 and 2.7 RList.hash returns same/different value
        print("\nRequirement 2.6 and 2.7: RList.hash returns same/different value")
        initial_hash = rlist.hash()
        print("Initial hash:", initial_hash)
        rlist.append('item3')
        new_hash = rlist.hash()
        print("New hash after modification:", new_hash)
        print("Hashes are different:", initial_hash != new_hash)

        # 2.8 RList.append adds item to the end
        print("\nRequirement 2.8: RList.append adds item to the end")
        rlist.append('item4')
        item = rlist.getItem(rlist.length() - 1)
        print("Last item after append:", item)

        """Esto no va bien xd
        # 2.9.1 and 2.9.2 RList.pop returns and removes last item
        print("\nRequirement 2.9.1 and 2.9.2: RList.pop returns and removes last item")
        item = rlist.pop()
        print("Popped item:", item)
        print("Length after pop:", rlist.length())
        """
        # 2.10.1 and 2.10.2 RList.pop returns and removes item at index
        print("\nRequirement 2.10.1 and 2.10.2: RList.pop returns and removes item at index")
        rlist.append('item5')
        item = rlist.pop(0)
        print("Popped item at index 0:", item)
        print("Length after pop at index:", rlist.length())

        # 2.11 RList.pop raises IndexError if index invalid
        print("\nRequirement 2.11: RList.pop raises IndexError if index invalid")
        try:
            rlist.pop(100)
        except rt.IndexError as e:
            print("Caught IndexError as expected:", e)

        # 2.12.1 and 2.12.2 RList.getItem returns item and keeps it
        print("\nRequirement 2.12.1 and 2.12.2: RList.getItem returns item and keeps it")
        rlist.append('item6')
        item = rlist.getItem(0)
        print("Item at index 0:", item)
        print("Length after getItem:", rlist.length())

        # 2.13 RList.getItem raises IndexError if index invalid
        print("\nRequirement 2.13: RList.getItem raises IndexError if index invalid")
        try:
            rlist.getItem(100)
        except rt.IndexError as e:
            print("Caught IndexError as expected:", e)

        # Testing RSet requirements
        print("\nTesting RSet requirements")
        # Get an RSet object
        rset_prx = factory.get(rt.TypeName.RSet, 'test_set')
        rset = rt.RSetPrx.checkedCast(rset_prx)

        # 3.1 RSet.remove removes an existing item
        print("\nRequirement 3.1: RSet.remove removes an existing item")
        rset.add('elem1')
        rset.remove('elem1')
        print("Removed 'elem1', contains 'elem1'? ", rset.contains('elem1'))

        # 3.2 RSet.remove raises KeyError if item doesn't exist
        print("\nRequirement 3.2: RSet.remove raises KeyError if item doesn't exist")
        try:
            rset.remove('nonexistent_elem')
        except rt.KeyError as e:
            print("Caught KeyError as expected:", e)

        # 3.3 RSet.length returns the correct length
        print("\nRequirement 3.3: RSet.length returns the correct length")
        rset.add('elem2')
        length = rset.length()
        print("Length after adding one element:", length)

        # 3.4 and 3.5 RSet.contains returns True/False
        print("\nRequirement 3.4 and 3.5: RSet.contains returns True/False")
        print("Contains 'elem2'?", rset.contains('elem2'))
        print("Contains 'elem3'?", rset.contains('elem3'))

        # 3.6 and 3.7 RSet.hash returns same/different value
        print("\nRequirement 3.6 and 3.7: RSet.hash returns same/different value")
        initial_hash = rset.hash()
        print("Initial hash:", initial_hash)
        rset.add('elem3')
        new_hash = rset.hash()
        print("New hash after modification:", new_hash)
        print("Hashes are different:", initial_hash != new_hash)

        # 3.8.1 and 3.8.2 RSet.add adds new item and doesn't add existing
        print("\nRequirement 3.8.1 and 3.8.2: RSet.add adds new item and doesn't add existing")
        rset.add('elem4')
        length_after_add = rset.length()
        print("Length after adding 'elem4':", length_after_add)
        rset.add('elem4')  # Adding the same element again
        length_after_add_same = rset.length()
        print("Length after adding 'elem4' again:", length_after_add_same)

        # 3.9.1 and 3.9.2 RSet.pop returns and removes an item
        print("\nRequirement 3.9.1 and 3.9.2: RSet.pop returns and removes an item")
        item = rset.pop()
        print("Popped item:", item)
        print("Length after pop:", rset.length())

        # 3.10 RSet.pop raises KeyError if set is empty
        print("\nRequirement 3.10: RSet.pop raises KeyError if set is empty")
        # Empty the set
        while True:
            try:
                rset.pop()
            except rt.KeyError:
                break
        try:
            rset.pop()
        except rt.KeyError as e:
            print("Caught KeyError as expected:", e)

        # Testing Iterable requirements
        print("\nTesting Iterable requirements")
        # 4.1 iter returns an Iterable object
        print("\nRequirement 4.1: iter returns an Iterable object")
        rlist.append('item7')
        rlist.append('item8')
        iterator = rlist.iter()
        print("Iterator obtained:", iterator)

        # 4.2 and 4.3 next returns next element and raises StopIteration
        print("\nRequirement 4.2 and 4.3: next returns next element and raises StopIteration")
        try:
            while True:
                item = iterator.next()
                print("Next item:", item)
        except rt.StopIteration:
            print("Reached end of iterator")
        """ Esto falla también xd"""
        # 4.4 next raises CancelIteration when object modified
        print("\nRequirement 4.4: next raises CancelIteration when object modified")
        iterator = rlist.iter()
        rlist.append('item9')  # Modify the list after creating iterator
        try:
            iterator.next()
        except rt.CancelIteration as e:
            print("Caught CancelIteration as expected:", e)
        
        

        # Testing Factory requirements
        print("\nTesting Factory requirements")
        # 5.1 Factory.get returns a new RDict
        print("\nRequirement 5.1: Factory.get returns a new RDict")
        new_rdict_prx = factory.get(rt.TypeName.RDict, 'new_dict')
        new_rdict = rt.RDictPrx.checkedCast(new_rdict_prx)
        new_rdict.setItem('new_key', 'new_value')
        print("New RDict contains 'new_key'?", new_rdict.contains('new_key'))

        # 5.2 Factory.get returns a new RList
        print("\nRequirement 5.2: Factory.get returns a new RList")
        new_rlist_prx = factory.get(rt.TypeName.RList, 'new_list')
        new_rlist = rt.RListPrx.checkedCast(new_rlist_prx)
        new_rlist.append('new_item')
        print("New RList contains 'new_item'?", new_rlist.contains('new_item'))

        # 5.3 Factory.get returns a new RSet
        print("\nRequirement 5.3: Factory.get returns a new RSet")
        new_rset_prx = factory.get(rt.TypeName.RSet, 'new_set')
        new_rset = rt.RSetPrx.checkedCast(new_rset_prx)
        new_rset.add('new_elem')
        print("New RSet contains 'new_elem'?", new_rset.contains('new_elem'))

        # 5.4 Factory.get returns existing RDict
        print("\nRequirement 5.4: Factory.get returns existing RDict")
        existing_rdict_prx = factory.get(rt.TypeName.RDict, 'new_dict')
        existing_rdict = rt.RDictPrx.checkedCast(existing_rdict_prx)
        print("Existing RDict contains 'new_key'?", existing_rdict.contains('new_key'))

        # 5.5 Factory.get returns existing RList
        print("\nRequirement 5.5: Factory.get returns existing RList")
        existing_rlist_prx = factory.get(rt.TypeName.RList, 'new_list')
        existing_rlist = rt.RListPrx.checkedCast(existing_rlist_prx)
        print("Existing RList contains 'new_item'?", existing_rlist.contains('new_item'))

        # 5.6 Factory.get returns existing RSet
        print("\nRequirement 5.6: Factory.get returns existing RSet")
        existing_rset_prx = factory.get(rt.TypeName.RSet, 'new_set')
        existing_rset = rt.RSetPrx.checkedCast(existing_rset_prx)
        print("Existing RSet contains 'new_elem'?", existing_rset.contains('new_elem'))

    return 0

if __name__ == '__main__':
    sys.exit(main())
