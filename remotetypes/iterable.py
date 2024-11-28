# iterable.py

import RemoteTypes as rt

class BaseIterable(rt.Iterable):
    """Clase base para las implementaciones de iterables."""

    def __init__(self, data: list[str], data_hash: int) -> None:
        """Inicializa el iterador con una copia de los datos y el hash actual."""
        self._data = data.copy()
        self._index = 0
        self._valid = True
        self._data_hash = data_hash

    def next(self, current=None) -> str:
        """Devuelve el siguiente elemento o lanza una excepción si no hay más."""
        if not self._valid:
            raise rt.CancelIteration("Iterator has been invalidated")  
        if self._index >= len(self._data):
            raise rt.StopIteration()
        item = self._data[self._index]
        self._index += 1
        return item


    def invalidate(self) -> None:
        """Invalida el iterador para que lance CancelIteration en la siguiente llamada a next."""
        self._valid = False

class ListIterable(BaseIterable):
    """Iterable para RemoteList."""
    pass

class DictIterable(BaseIterable):
    """Iterable para RemoteDict."""
    pass

class SetIterable(BaseIterable):
    """Iterable para RemoteSet."""
    pass
