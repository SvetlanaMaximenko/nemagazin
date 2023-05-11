from typing import Callable, Optional

from .models import User
from .storage import AbstractStorage


class UserMenu:
    def __init__(self, storage: AbstractStorage):
        self._menu_list = []
        self._storage = storage

    def get_current_user(self) -> Optional[User]:
        return self._storage.get("user")

    def add_menu_category(self, name: str, callback: Callable, login_required: bool):
        self._menu_list.append(
            {
                "login_required": login_required,
                "name": name,
                "callback": callback,
            }
        )

    def display_categories(self):
        for i, cat in enumerate(self._menu_list, 1):
            if cat["login_required"] and self.get_current_user() is None:
                continue
            print(f" {i}. {cat['name']}")

    def handler(self):
        index = input(" > ")
        if not index.isdigit():
            return
        index = int(index)
        if index < 1 or index > len(self._menu_list):
            return

        self._menu_list[index - 1]["callback"]()
