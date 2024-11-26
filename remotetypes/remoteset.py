# remoteset.py

import os
import json
from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

from remotetypes.iterable import SetIterable  # Necesitaremos implementar esto
from remotetypes.customset import StringSet

class RemoteSet(rt.RSet):
    """Implementación de la interfaz remota RSet."""

    def __init__(self, identifier: Optional[str] = None, persistence_dir: str = 'data') -> None:
        """Inicializa un RemoteSet con un StringSet vacío o carga su estado si tiene un identificador."""
        self._storage = StringSet()
        self._iterators = set()
        self._hash = self._compute_hash()
        self._identifier = identifier
        self._persistence_dir = persistence_dir
        if self._identifier:
            self._load_state()

    def _compute_hash(self) -> int:
        """Calcula un hash basado en el contenido del conjunto."""
        return hash(frozenset(self._storage))

    def _get_persistence_path(self) -> str:
        """Obtiene la ruta completa del archivo de persistencia."""
        filename = f"{self._identifier}.json"
        return os.path.join(self._persistence_dir, filename)

    def _load_state(self) -> None:
        """Carga el estado del conjunto desde el archivo de persistencia."""
        path = self._get_persistence_path()
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                self._storage = StringSet(data)
                self._hash = self._compute_hash()

    def _save_state(self) -> None:
        """Guarda el estado del conjunto en el archivo de persistencia."""
        path = self._get_persistence_path()
        os.makedirs(self._persistence_dir, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(list(self._storage), f)

    def _invalidate_iterators(self) -> None:
        """Invalida todos los iteradores activos."""
        for iterator in self._iterators:
            iterator.invalidate()
        self._iterators.clear()

    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Añade un elemento al conjunto."""
        self._storage.add(item)
        self._hash = self._compute_hash()
        self._invalidate_iterators()
        if self._identifier:
            self._save_state()

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Elimina un elemento del conjunto."""
        try:
            self._storage.remove(item)
            self._hash = self._compute_hash()
            self._invalidate_iterators()
            if self._identifier:
                self._save_state()
        except KeyError as error:
            raise rt.KeyError(f"Item '{item}' not found") from error

    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """Elimina y devuelve un elemento del conjunto."""
        try:
            item = self._storage.pop()
            self._hash = self._compute_hash()
            self._invalidate_iterators()
            if self._identifier:
                self._save_state()
            return item
        except KeyError as error:
            raise rt.KeyError("Set is empty") from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Devuelve el número de elementos en el conjunto."""
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Comprueba si el elemento está en el conjunto."""
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Devuelve el hash actual del conjunto."""
        return self._hash

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Crea y devuelve un iterador sobre los elementos del conjunto."""
        iterator = SetIterable(list(self._storage), self._hash)
        proxy = current.adapter.addWithUUID(iterator)
        self._iterators.add(iterator)
        return rt.IterablePrx.uncheckedCast(proxy)
