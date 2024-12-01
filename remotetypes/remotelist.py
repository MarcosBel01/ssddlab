"""
Este módulo implementa la clase RemoteDict, que proporciona una
interfaz remota para un diccionario distribuido utilizando Ice.
"""

from typing import Optional
import os
import json
import Ice
#pylint: disable=import-error
import RemoteTypes as rt  # noqa: F401;
from remotetypes.iterable import ListIterable  

class RemoteList(rt.RList):
    """
    Clase RemoteDict que implementa la interfaz remota RDict.

    Permite almacenar y manipular un diccionario remoto de forma distribuida.
    """

    def __init__(self, identifier: Optional[str] = None, persistence_dir: str = 'data') -> None:
        """
        Inicializa un RemoteDict con un diccionario vacío o 
        carga su estado si tiene un identificador.

        Args:
            identifier (Optional[str]): Identificador del diccionario remoto.
            persistence_dir (str): Directorio donde se guardará el estado.
        """
        self._storage = []
        self._iterators = set()
        self._hash = self._compute_hash()
        self._identifier = identifier
        self._persistence_dir = persistence_dir
        if self._identifier:
            self._load_state()

    def _compute_hash(self) -> int:
        """Calcula un hash basado en el contenido de la lista."""
        return hash(tuple(self._storage))

    def _get_persistence_path(self) -> str:
        """Obtiene la ruta completa del archivo de persistencia."""
        filename = f"{self._identifier}.json"
        return os.path.join(self._persistence_dir, filename)

    def _load_state(self) -> None:
        """Carga el estado de la lista desde el archivo de persistencia."""
        path = self._get_persistence_path()
        if os.path.exists(path):
            with open(path, 'r',encoding='utf-8') as f:
                self._storage = json.load(f)
                self._hash = self._compute_hash()

    def _save_state(self) -> None:
        """Guarda el estado de la lista en el archivo de persistencia."""
        path = self._get_persistence_path()
        os.makedirs(self._persistence_dir, exist_ok=True)
        with open(path, 'w',encoding='utf-8') as f:
            json.dump(self._storage, f)

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Elimina la primera ocurrencia de item en la lista."""
        try:
            self._storage.remove(item)
            self._hash = self._compute_hash()
            self._invalidate_iterators()
            if self._identifier:
                self._save_state()
        except ValueError as error:
            raise rt.KeyError(f"Item '{item}' not found") from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Devuelve el número de elementos en la lista."""
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Devuelve True si item está en la lista."""
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Devuelve el hash actual de la lista."""
        return self._hash

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Crea y devuelve un iterador sobre la lista."""
        iterator = ListIterable(self._storage, self._hash)
        proxy = current.adapter.addWithUUID(iterator)
        self._iterators.add(iterator)
        return rt.IterablePrx.uncheckedCast(proxy)

    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Añade un elemento al final de la lista."""
        self._storage.append(item)
        self._hash = self._compute_hash()
        self._invalidate_iterators()
        if self._identifier:
            self._save_state()

    def pop(self, index=None, current=None):
        """Elimina y devuelve el elemento en la posición index, o el último si no se proporciona."""
        try:
            if index is None or index is Ice.Unset:
                index = -1  # Último elemento
            item = self._storage.pop(index)
            self._hash = self._compute_hash()
            self._invalidate_iterators()
            if self._identifier:
                self._save_state()
            return item
        except IndexError as error:
            raise rt.IndexError("Index out of range") from error



    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        """Devuelve el elemento en la posición index."""
        try:
            return self._storage[index]
        except IndexError as error:
            raise rt.IndexError("Index out of range") from error

    def _invalidate_iterators(self) -> None:
        """Invalida todos los iteradores activos."""
        for iterator in self._iterators:
            iterator.invalidate()
        self._iterators.clear()
