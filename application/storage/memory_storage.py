from .base import AbstractStorage


class MemoryStorage(AbstractStorage):
    """
    Класс MemoryStorage — это реализация интерфейса AbstractStorage, который хранит элементы в памяти.
    """

    def __init__(self):
        self._items = {}

    def get(self, name: str):
        return self._items.get(name, None)

    def set(self, name: str, item):
        self._items[name] = item

    def delete(self, name: str):
        del self._items[name]
