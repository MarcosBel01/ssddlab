import unittest
import os
import Ice
from unittest.mock import Mock
from remotetypes.remotelist import RemoteList
import RemoteTypes as rt  # Importar excepciones si es necesario

class TestRemoteList(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada prueba."""
        # Inicializar el comunicador y el adaptador
        self.communicator = Ice.initialize([])
        self.adapter = self.communicator.createObjectAdapter("TestAdapter")
        self.adapter.activate()

        # Usamos un identificador único para evitar conflictos
        self.identifier = 'test_list'
        self.persistence_dir = 'test_data'
        self.remote_list = RemoteList(identifier=self.identifier, persistence_dir=self.persistence_dir)
        
        # Asegurarnos de que el estado esté limpio
        self._cleanup_persistence()

    def tearDown(self):
        """Se ejecuta después de cada prueba."""
        # Limpiar los datos de persistencia
        self._cleanup_persistence()
        # Desactivar y destruir el adaptador
        self.adapter.destroy()
        # Finalizar el comunicador
        self.communicator.destroy()

    def _cleanup_persistence(self):
        """Elimina el archivo de persistencia si existe."""
        path = self.remote_list._get_persistence_path()
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(self.persistence_dir) and not os.listdir(self.persistence_dir):
            os.rmdir(self.persistence_dir)

    # ... (otras pruebas) ...

    def test_iterator(self):
        """Prueba que el iterador recorre todos los elementos."""
        items = ['item1', 'item2', 'item3']
        for item in items:
            self.remote_list.append(item)

        # Crear un mock de 'current' con el adaptador
        mock_current = Mock()
        mock_current.adapter = self.adapter

        iterator_prx = self.remote_list.iter(current=mock_current)
        iterated_items = []
        try:
            while True:
                item = iterator_prx.next()
                iterated_items.append(item)
        except rt.StopIteration:
            pass
        except rt.CancelIteration:
            self.fail('El iterador fue invalidado inesperadamente')

        self.assertEqual(iterated_items, items)

    def test_iterator_invalidation(self):
        """Prueba que el iterador se invalida cuando la lista cambia."""
        self.remote_list.append('item1')

        # Crear un mock de 'current' con el adaptador
        mock_current = Mock()
        mock_current.adapter = self.adapter

        iterator_prx = self.remote_list.iter(current=mock_current)
        self.remote_list.append('item2')  # Esto debe invalidar el iterador
        with self.assertRaises(rt.CancelIteration):
            iterator_prx.next()

    # ... (otras pruebas) ...

if __name__ == '__main__':
    unittest.main()

