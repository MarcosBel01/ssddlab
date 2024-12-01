"""
Módulo Factory para gestionar la creación y recuperación de objetos remotos.
"""

# pylint: disable=import-error
import RemoteTypes as rt  # noqa: F401
from remotetypes.remotelist import RemoteList
from remotetypes.remotedict import RemoteDict
from remotetypes.remoteset import RemoteSet


class Factory(rt.Factory):
    """Clase Factory para manejar la creación de proxies de objetos remotos."""

    def __init__(self, adapter, persistence_dir='data'):
        self._objects = {}
        self._adapter = adapter
        self._persistence_dir = persistence_dir

    def get(self, typeName, identifier=None, current=None):
        """
        Obtiene un objeto remoto según el tipo y el identificador.

        Args:
            type_name (TypeName): El tipo de objeto remoto a obtener.
            current: Contexto actual de Ice.

        Returns:
            RTypePrx: Proxy al objeto remoto solicitado.

        Raises:
            ValueError: Si se solicita un tipo inválido.
        """
        if identifier and identifier in self._objects:
            return self._objects[identifier]
        else:
            if typeName == rt.TypeName.RList:
                obj = RemoteList(identifier=identifier, persistence_dir=self._persistence_dir)
            elif typeName == rt.TypeName.RDict:
                obj = RemoteDict(identifier=identifier, persistence_dir=self._persistence_dir)
            elif typeName == rt.TypeName.RSet:
                obj = RemoteSet(identifier=identifier, persistence_dir=self._persistence_dir)
            else:
                raise ValueError("Unknown TypeName")

            proxy = self._adapter.addWithUUID(obj)
            prx = rt.RTypePrx.uncheckedCast(proxy)

            if identifier:
                self._objects[identifier] = prx

            return prx
