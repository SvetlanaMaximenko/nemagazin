from typing import Callable, Optional

from .models import User
from .storage import AbstractStorage


class UserMenu:
    def __init__(self, storage: AbstractStorage):
        self._menu_list = []
        self._storage = storage

    def get_current_user(self) -> Optional[User]:
        """
        Если в storage есть ключ user, то возвращается соответствующее значение (объект User).
        Если ключ «user» отсутствует в storage, то возвращается «None».
        """
        return self._storage.get("user")

    def add_menu_category(self, name: str, callback: Callable, login_required: int):
        """
        Эта функция добавляет категорию меню в список с именем, функцией обратного вызова и флагом, указывающим,
        требуется ли вход в систему.

        :param name: Название категории меню, которое будет отображаться пользователю.
        :param callback: Параметр «обратный вызов» — это функция, которая будет вызываться при выборе пользователем
         категории меню. Это тип Callable, что означает, что это может быть любой объект,
         который можно вызывать как функцию. Функция не должна принимать аргументы и ничего не возвращать.
        :param login_required: Параметр `login_required` представляет собой логическое значение, указывающее, должен ли
         пользователь войти в систему для доступа к категории меню.
        """
        self._menu_list.append(
            {
                "login_required": login_required,
                "name": name,
                "callback": callback,
            }
        )

    def display_categories(self):
        """
        Эта функция отображает категории меню, пропуская те, которые требуют входа в систему, если пользователь в данный
        момент не вошел в систему.
        """
        for i, cat in enumerate(self._menu_list, 1):
            if (cat["login_required"]) == 0:
                print(f" {i}. {cat['name']}")
            if self.get_current_user() and cat["login_required"] == 2:
                print(f" {i}. {cat['name']}")
            elif self.get_current_user() is None and cat["login_required"] == 1:
                print(f" {i}. {cat['name']}")

    def handler(self):
        """
        Функция принимает пользовательский ввод, проверяет, является ли он допустимым индексом,
        и вызывает соответствующую функцию обратного вызова из списка.

        Если входной индекс не является цифрой или выходит за пределы допустимого диапазона (меньше 1 или больше
        длины списка меню), то ничего не возвращается (неявно возвращает None). В противном случае вызывается функция,
        связанная с выбранным пунктом меню.
        """
        index = input(" > ")
        if not index.isdigit():
            return
        index = int(index)
        if index < 1 or index > len(self._menu_list):
            return

        self._menu_list[index - 1]["callback"]()
