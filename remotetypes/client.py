#Cliente para probar los requisitos que se piden en "requisitos.md"
import sys
import Ice
import RemoteTypes as rt

def main():
    with Ice.initialize(sys.argv) as communicator:
        # Configurar el proxy para la factoría
        factory_proxy = communicator.stringToProxy("Factory:tcp -h localhost -p 10000")
        factory = rt.FactoryPrx.checkedCast(factory_proxy)
        if not factory:
            print('Proxy de la factoría inválido')
            return 1

        print("Probando requisitos de RDict")
        # Obtener un objeto RDict
        rdict_prx = factory.get(rt.TypeName.RDict, 'test_dict')
        rdict = rt.RDictPrx.checkedCast(rdict_prx)

        # 1.1 RDict.remove borra un elemento por clave
        print("\nRequisito 1.1: RDict.remove borra un elemento por clave")
        rdict.setItem('key1', 'value1')
        rdict.remove('key2')
        print("Se eliminó 'key1', ¿contiene 'key1'?", rdict.contains('key1'))

        # 1.2 RDict.remove lanza KeyError si la clave no existe
        print("\nRequisito 1.2: RDict.remove lanza KeyError si la clave no existe")
        try:
            rdict.remove('nonexistent_key')
        except rt.KeyError as e:
            print("KeyError capturado como se esperaba:", e)

        # 1.3 RDict.length devuelve la longitud correcta
        print("\nRequisito 1.3: RDict.length devuelve la longitud correcta")
        rdict.setItem('key2', 'value2')
        length = rdict.length()
        print("Longitud tras añadir un elemento:", length)

        # 1.4 y 1.5 RDict.contains devuelve True/False
        print("\nRequisito 1.4 y 1.5: RDict.contains devuelve True/False")
        print("¿Contiene 'key2'?", rdict.contains('key2'))
        print("¿Contiene 'key3'?", rdict.contains('key3'))

        # 1.6 y 1.7 RDict.hash devuelve valores iguales/diferentes
        print("\nRequisito 1.6 y 1.7: RDict.hash devuelve valores iguales/diferentes")
        initial_hash = rdict.hash()
        print("Hash inicial:", initial_hash)
        rdict.setItem('key3', 'value3')
        new_hash = rdict.hash()
        print("Nuevo hash tras modificación:", new_hash)
        print("¿Los hashes son diferentes?", initial_hash != new_hash)

        # 1.8 RDict.setItem permite recuperar la clave
        print("\nRequisito 1.8: RDict.setItem permite recuperar la clave")
        rdict.setItem('key4', 'value4')
        value = rdict.getItem('key4')
        print("Clave 'key4' recuperada con valor:", value)

        # 1.9 RDict.getItem lanza KeyError si la clave no existe
        print("\nRequisito 1.9: RDict.getItem lanza KeyError si la clave no existe")
        try:
            rdict.getItem('nonexistent_key')
        except rt.KeyError as e:
            print("KeyError capturado como se esperaba:", e)

        # 1.10.1 y 1.10.2 RDict.getItem devuelve y mantiene el valor
        print("\nRequisito 1.10.1 y 1.10.2: RDict.getItem devuelve y mantiene el valor")
        value = rdict.getItem('key2')
        print("Valor recuperado para 'key2':", value)
        print("¿Contiene 'key2' tras getItem?", rdict.contains('key2'))

        # 1.11 RDict.pop lanza KeyError si la clave no existe
        print("\nRequisito 1.11: RDict.pop lanza KeyError si la clave no existe")
        try:
            rdict.pop('nonexistent_key')
        except rt.KeyError as e:
            print("KeyError capturado como se esperaba:", e)

        # 1.12.1 y 1.12.2 RDict.pop devuelve y elimina el valor
        print("\nRequisito 1.12.1 y 1.12.2: RDict.pop devuelve y elimina el valor")
        rdict.setItem('key5', 'value5')
        value = rdict.pop('key5')
        print("Clave 'key5' eliminada con valor:", value)
        print("¿Contiene 'key5' tras pop?", rdict.contains('key5'))

         # Probando requisitos de RList
        print("\nProbando requisitos de RList")
        # Obtener un objeto RList
        rlist_prx = factory.get(rt.TypeName.RList, 'test_list')
        rlist = rt.RListPrx.checkedCast(rlist_prx)

        # 2.1 RList.remove borra un elemento por valor
        print("\nRequisito 2.1: RList.remove borra un elemento por valor")
        rlist.append('item1')
        rlist.remove('item1')
        print("Se eliminó 'item1', ¿contiene 'item1'?", rlist.contains('item1'))

        # 2.2 RList.remove lanza KeyError si el elemento no existe
        print("\nRequisito 2.2: RList.remove lanza KeyError si el elemento no existe")
        try:
            rlist.remove('nonexistent_item')
        except rt.KeyError as e:
            print("KeyError capturado como se esperaba:", e)

        # 2.3 RList.length devuelve la longitud correcta
        print("\nRequisito 2.3: RList.length devuelve la longitud correcta")
        rlist.append('item2')
        length = rlist.length()
        print("Longitud tras añadir un elemento:", length)

        # 2.4 y 2.5 RList.contains devuelve True/False
        print("\nRequisito 2.4 y 2.5: RList.contains devuelve True/False")
        print("¿Contiene 'item2'?", rlist.contains('item2'))
        print("¿Contiene 'item3'?", rlist.contains('item3'))

        # 2.6 y 2.7 RList.hash devuelve valores iguales/diferentes
        print("\nRequisito 2.6 y 2.7: RList.hash devuelve valores iguales/diferentes")
        initial_hash = rlist.hash()
        print("Hash inicial:", initial_hash)
        rlist.append('item3')
        new_hash = rlist.hash()
        print("Nuevo hash tras modificación:", new_hash)
        print("¿Los hashes son diferentes?", initial_hash != new_hash)

        # 2.8 RList.append añade un elemento al final
        print("\nRequisito 2.8: RList.append añade un elemento al final")
        rlist.append('item4')
        item = rlist.getItem(rlist.length() - 1)
        print("Último elemento tras append:", item)

        # 2.9.1 y 2.9.2 RList.pop devuelve y elimina el último elemento
        print("\nRequisito 2.9.1 y 2.9.2: RList.pop devuelve y elimina el último elemento")
        item = rlist.pop()
        print("Elemento eliminado:", item)
        print("Longitud tras pop:", rlist.length())

        # 2.10.1 y 2.10.2 RList.pop devuelve y elimina un elemento por índice
        print("\nRequisito 2.10.1 y 2.10.2: RList.pop devuelve y elimina un elemento por índice")
        rlist.append('item5')
        item = rlist.pop(0)
        print("Elemento eliminado en el índice 0:", item)
        print("Longitud tras pop en índice:", rlist.length())

        # 2.11 RList.pop lanza IndexError si el índice es inválido
        print("\nRequisito 2.11: RList.pop lanza IndexError si el índice es inválido")
        try:
            rlist.pop(100)
        except rt.IndexError as e:
            print("IndexError capturado como se esperaba:", e)

        # 2.12.1 y 2.12.2 RList.getItem devuelve y mantiene un elemento por índice
        print("\nRequisito 2.12.1 y 2.12.2: RList.getItem devuelve y mantiene un elemento por índice")
        rlist.append('item6')
        item = rlist.getItem(0)
        print("Elemento en índice 0:", item)
        print("Longitud tras getItem:", rlist.length())

        # 2.13 RList.getItem lanza IndexError si el índice es inválido
        print("\nRequisito 2.13: RList.getItem lanza IndexError si el índice es inválido")
        try:
            rlist.getItem(100)
        except rt.IndexError as e:
            print("IndexError capturado como se esperaba:", e)

        # Probando requisitos de RSet
        print("\nProbando requisitos de RSet")
        # Obtener un objeto RSet
        rset_prx = factory.get(rt.TypeName.RSet, 'test_set')
        rset = rt.RSetPrx.checkedCast(rset_prx)

        # 3.1 RSet.remove borra un elemento por valor
        print("\nRequisito 3.1: RSet.remove borra un elemento por valor")
        rset.add('elem1')
        rset.remove('elem1')
        print("Se eliminó 'elem1', ¿contiene 'elem1'?", rset.contains('elem1'))

        # 3.2 RSet.remove lanza KeyError si el elemento no existe
        print("\nRequisito 3.2: RSet.remove lanza KeyError si el elemento no existe")
        try:
            rset.remove('nonexistent_elem')
        except rt.KeyError as e:
            print("KeyError capturado como se esperaba:", e)

        # 3.3 RSet.length devuelve la longitud correcta
        print("\nRequisito 3.3: RSet.length devuelve la longitud correcta")
        rset.add('elem2')
        length = rset.length()
        print("Longitud tras añadir un elemento:", length)

        # 3.4 y 3.5 RSet.contains devuelve True/False
        print("\nRequisito 3.4 y 3.5: RSet.contains devuelve True/False")
        print("¿Contiene 'elem2'?", rset.contains('elem2'))
        print("¿Contiene 'elem3'?", rset.contains('elem3'))

        # 3.6 y 3.7 RSet.hash devuelve valores iguales/diferentes
        print("\nRequisito 3.6 y 3.7: RSet.hash devuelve valores iguales/diferentes")
        initial_hash = rset.hash()
        print("Hash inicial:", initial_hash)
        rset.add('elem3')
        new_hash = rset.hash()
        print("Nuevo hash tras modificación:", new_hash)
        print("¿Los hashes son diferentes?", initial_hash != new_hash)

        # 3.8.1 y 3.8.2 RSet.add añade nuevos elementos y no añade duplicados
        print("\nRequisito 3.8.1 y 3.8.2: RSet.add añade nuevos elementos y no añade duplicados")
        rset.add('elem4')
        length_after_add = rset.length()
        print("Longitud tras añadir 'elem4':", length_after_add)
        rset.add('elem4')  # Añadir el mismo elemento nuevamente
        length_after_add_same = rset.length()
        print("Longitud tras añadir 'elem4' otra vez:", length_after_add_same)

        # 3.9.1 y 3.9.2 RSet.pop devuelve y elimina un elemento
        print("\nRequisito 3.9.1 y 3.9.2: RSet.pop devuelve y elimina un elemento")
        item = rset.pop()
        print("Elemento eliminado:", item)
        print("Longitud tras pop:", rset.length())

        # 3.10 RSet.pop lanza KeyError si el conjunto está vacío
        print("\nRequisito 3.10: RSet.pop lanza KeyError si el conjunto está vacío")
        # Vaciar el conjunto
        while True:
            try:
                rset.pop()
            except rt.KeyError:
                break
        try:
            rset.pop()
        except rt.KeyError as e:
            print("KeyError capturado como se esperaba:", e)

        # Probando requisitos de Iterable
        print("\nProbando requisitos de Iterable")

        # 4.1 iter devuelve un objeto de tipo Iterable
        print("\nRequisito 4.1: iter devuelve un objeto de tipo Iterable")
        rlist.append('item7')
        rlist.append('item8')
        iterator = rlist.iter()
        print("Iterador obtenido:", iterator)

        # 4.2 y 4.3 next devuelve el siguiente elemento y lanza StopIteration
        print("\nRequisito 4.2 y 4.3: next devuelve el siguiente elemento y lanza StopIteration")
        try:
            while True:
                item = iterator.next()
                print("Siguiente elemento:", item)
        except rt.StopIteration:
            print("Se alcanzó el final del iterador")

        # 4.4 next lanza CancelIteration si el objeto es modificado
        print("\nRequisito 4.4: next lanza CancelIteration si el objeto es modificado")
        iterator = rlist.iter()
        rlist.append('item9')  # Modificar la lista después de crear el iterador
        try:
            iterator.next()
        except rt.CancelIteration as e:
            print("CancelIteration capturado como se esperaba:", e)

        # Probando requisitos de Factory
        print("\nProbando requisitos de Factory")

        # 5.1 Factory.get devuelve un nuevo RDict
        print("\nRequisito 5.1: Factory.get devuelve un nuevo RDict")
        new_rdict_prx = factory.get(rt.TypeName.RDict, 'new_dict')
        new_rdict = rt.RDictPrx.checkedCast(new_rdict_prx)
        new_rdict.setItem('new_key', 'new_value')
        print("¿El nuevo RDict contiene 'new_key'?", new_rdict.contains('new_key'))

        # 5.2 Factory.get devuelve un nuevo RList
        print("\nRequisito 5.2: Factory.get devuelve un nuevo RList")
        new_rlist_prx = factory.get(rt.TypeName.RList, 'new_list')
        new_rlist = rt.RListPrx.checkedCast(new_rlist_prx)
        new_rlist.append('new_item')
        print("¿El nuevo RList contiene 'new_item'?", new_rlist.contains('new_item'))

        # 5.3 Factory.get devuelve un nuevo RSet
        print("\nRequisito 5.3: Factory.get devuelve un nuevo RSet")
        new_rset_prx = factory.get(rt.TypeName.RSet, 'new_set')
        new_rset = rt.RSetPrx.checkedCast(new_rset_prx)
        new_rset.add('new_elem')
        print("¿El nuevo RSet contiene 'new_elem'?", new_rset.contains('new_elem'))

        # 5.4 Factory.get devuelve un RDict existente
        print("\nRequisito 5.4: Factory.get devuelve un RDict existente")
        existing_rdict_prx = factory.get(rt.TypeName.RDict, 'new_dict')
        existing_rdict = rt.RDictPrx.checkedCast(existing_rdict_prx)
        print("¿El RDict existente contiene 'new_key'?", existing_rdict.contains('new_key'))

        # 5.5 Factory.get devuelve un RList existente
        print("\nRequisito 5.5: Factory.get devuelve un RList existente")
        existing_rlist_prx = factory.get(rt.TypeName.RList, 'new_list')
        existing_rlist = rt.RListPrx.checkedCast(existing_rlist_prx)
        print("¿El RList existente contiene 'new_item'?", existing_rlist.contains('new_item'))

        # 5.6 Factory.get devuelve un RSet existente
        print("\nRequisito 5.6: Factory.get devuelve un RSet existente")
        existing_rset_prx = factory.get(rt.TypeName.RSet, 'new_set')
        existing_rset = rt.RSetPrx.checkedCast(existing_rset_prx)
        print("¿El RSet existente contiene 'new_elem'?", existing_rset.contains('new_elem'))

    return 0

if __name__ == '__main__':
    sys.exit(main())
