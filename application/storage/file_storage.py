from .base import AbstractStorage


class FileStorage(AbstractStorage):

    def __init__(self, file_name):
        self._file_name = file_name

    def get(self, name: str):
        with open(self._file_name) as f:
            pass

    def set(self, name: str, item):
        with open(self._file_name, "w") as f:
            pass

    def delete(self, name: str):
        with open(self._file_name, "w") as f:
            pass
