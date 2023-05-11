from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    """
    Приведенный выше класс является абстрактным классом с тремя абстрактными методами
    для получения, установки и удаления элементов из хранилища.
    """

    @abstractmethod
    def get(self, name: str):
        pass

    @abstractmethod
    def set(self, name: str, item):
        pass

    @abstractmethod
    def delete(self, name: str):
        pass
