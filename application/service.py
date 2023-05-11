from datetime import datetime

import tabulate

from application.storage import AbstractStorage
from .models import Ticket, Product, User, Orders


class ShopService:
    def __init__(self, storage: AbstractStorage):
        self._storage = storage
        self._user: User = None

    @staticmethod
    def display_products() -> None:
        products = [[p.id, p.cost, p.count, p.name] for p in Product.all()]
        print(
            tabulate.tabulate(
                products, headers=["ID", "Стоимость", "Кол-во", "Название"]
            )
        )

    def register(self) -> None:
        while True:
            username = input("> Введите username: ")
            if User.is_exist(username=username):
                print(" Такой username уже существует, укажите другой!")
                continue

            password = input("> Введите password: ")
            if len(password) < 8:
                print("Пароль должен быть не менее 8 символов")
                continue

            break

        user = User.create(username=username, password=password, points=0)
        self._login_user(user)

    def login(self) -> None:
        while True:
            username = input("> Введите username: ")
            if not User.is_exist(username=username):
                print(" Такой username не существует!")
                return

            password = input("> Введите password: ")
            user = User.get(username=username, password=password)
            if user is None:
                print("Неверный пароль!")
                continue
            break

        self._login_user(user)

    def _login_user(self, user: User) -> None:
        self._storage.set(name="user", item=user)
        self._user = user

    def _update_user(self, user: User) -> None:
        self._storage.set(name="user", item=user)

    def submit_ticket(self) -> None:
        ticket_uuid = input("> Введите ticket: ")
        if not Ticket.is_valid(ticket_uuid):
            print(" Неверный ticket!")
            return

        ticket: Ticket = Ticket.get(uuid=ticket_uuid)

        self._user.points += 20
        self._user.update(points=self._user.points)
        self._update_user(self._user)

        ticket.update(available=False, user=self._user.id)

        print(" Было добавлено 20 поинтов")

    def buy_product(self) -> None:
        product_id = input(" Укажите ID товара: ")
        if not product_id.isdigit():
            print("ID должен быть числом")
            return

        product: Product = Product.get(id=int(product_id))
        if product is None:
            print("Такого продукта не существует")
            return

        if self._user.points < product.cost:
            print("У вас недостаточно поинтов")
            return

        Orders.create(
            user=self._user,
            product=product,
            count=1,
            order_datetime=datetime.now(),
        )

        self._user.points -= product.cost
        self._user.update(points=self._user.points)
        product.update(count=product.count-1)
        self._update_user(self._user)

        print(f"Спасибо, что купили {product.name}")

    def profile(self):
        print(f" Ваш профиль: \n {self._user.username}\n Points: {self._user.points}")

        orders = Orders.filter(user_id=self._user.id)

        if not orders:
            print(" У вас нет заказов")
        else:
            print(
                tabulate.tabulate(
                    [
                        [
                            o.id,
                            Product.get(id=o.product_id).name,
                            o.count,
                            o.order_datetime,
                        ]
                        for o in orders
                    ],
                    headers=["ID", "Название", "Кол-во", "Дата и время заказа"],
                )
            )
