# conftest.py
import pytest
import Ice

@pytest.fixture(scope='module')
def ice_communicator():
    # Inicializar el comunicador de Ice
    communicator = Ice.initialize()
    yield communicator
    # Destruir el comunicador después de las pruebas
    communicator.destroy()

@pytest.fixture(scope='module')
def ice_adapter(ice_communicator):
    # Crear un adaptador de objetos
    adapter = ice_communicator.createObjectAdapterWithEndpoints("TestAdapter", "tcp -h 127.0.0.1 -p 0")
    adapter.activate()
    yield adapter
    # Desactivar el adaptador después de las pruebas
    adapter.deactivate()
    adapter.waitForDeactivate()
