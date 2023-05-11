from abc import ABC, abstractmethod


class AbstractStorage(ABC):

    @abstractmethod
    def get(self, name: str):
        pass

    @abstractmethod
    def set(self, name: str, item):
        pass

    @abstractmethod
    def delete(self, name: str):
        pass
