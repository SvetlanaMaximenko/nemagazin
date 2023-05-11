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
        """
        Функция отображает таблицу информации о продукте, включая идентификатор, стоимость, количество и название.
        """

        # Метод `Product.all()` возвращает список всех продуктов в системе, далее создается список для извлечения
        # соответствующей информации для каждого продукта и создания нового списка списков.
        # Затем этот список используется для отображения информации о продуктах в отформатированной таблице
        # с помощью функции `tabulate.tabulate()`.
        products = [[p.id, p.cost, p.count, p.name] for p in Product.all()]

        print(
            tabulate.tabulate(
                products, headers=["ID", "Стоимость", "Кол-во", "Название"]
            )
        )

    def register(self) -> None:
        """
        Этот метод реализует процесс регистрации нового пользователя. Он предлагает пользователю ввести уникальное
        имя пользователя и пароль длиной не менее 8 символов. Затем он проверяет, существует ли уже введенное имя
        пользователя в системе, и предлагает пользователю ввести другое имя пользователя, если оно уже существует.

        Если имя пользователя уникально, он проверяет, содержит ли введенный пароль не менее 8 символов, и предлагает
        пользователю ввести новый пароль, если это не так.

        Как только пользователь вводит уникальное имя пользователя и пароль длиной не менее 8 символов,
        цикл прерывается и создается новый пользователь с введенным именем пользователя и паролем и 0 points.
        """

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
        # `self._login_user(user)` — это метод, который устанавливает текущего пользователя для предоставленного
        # пользователя и сохраняет его в объекте `_storage`. Он вызывается после того, как пользователь успешно войдет в
        # систему или зарегистрируется.
        self._login_user(user)

    def login(self) -> None:
        """
        Этот метод реализует функцию входа в систему для пользователя.

        Он предлагает пользователю ввести свое имя пользователя и пароль, проверяет, существует ли имя пользователя
        в системе, и если существует, проверяет правильность пароля.

        Если пароль неверный, пользователю предлагается ввести пароль еще раз.

        Этот процесс продолжается до тех пор, пока не будут введены правильные имя пользователя и пароль, после
        чего пользователь войдет в систему.
        """

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
        """
        Это закрытый метод, который регистрирует пользователя и принимает объект User в качестве входных данных.
        """
        self._storage.set(name="user", item=user)
        self._user = user

    def _update_user(self, user: User) -> None:
        """
        Это закрытый метод, который обновляет пользовательский объект.
        """
        self._storage.set(name="user", item=user)

    def submit_ticket(self) -> None:
        """
        Эта функция позволяет пользователю применить ticket, проверит его, обновит points пользователя и обновит
        доступность ticket'а и информацию о пользователе.
        """
        ticket_uuid = input("> Введите ticket: ")
        if not Ticket.is_valid(ticket_uuid):
            print(" Неверный ticket!")
            return

        ticket: Ticket = Ticket.get(uuid=ticket_uuid)

        # Эти строки кода обновляют points текущего пользователя, добавляя 20 points, а затем обновляя объект
        # пользователя в хранилище новым значением баллов. Это делается, когда пользователь отправляет
        # действительный ticket.
        self._user.points += 20
        self._user.update(points=self._user.points)
        self._update_user(self._user)

        ticket.update(available=False, user=self._user.id)

        print(" Было добавлено 20 поинтов")

    def buy_product(self) -> None:
        """
        Эта функция позволяет пользователю покупать продукт, проверяя, достаточно ли у него points, создавая заказ и
        обновляя points пользователя и уменьшает количество продукта.
        """

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

        # Эти строки кода обновляют points пользователя, вычитая стоимость продукта, который они покупают,
        # обновляют points пользователя, уменьшают количество продуктов на 1 и обновляют информацию о
        # пользователе в хранилище.
        self._user.points -= product.cost
        self._user.update(points=self._user.points)
        product.update(count=product.count-1)
        self._update_user(self._user)

        print(f"Спасибо, что купили {product.name}")

    def profile(self):
        """
        Функция выводит информацию о профиле пользователя и историю его заказов, если таковая имеется.
        """

        print(f" Ваш профиль: \n {self._user.username}\n Points: {self._user.points}")

        orders = Orders.filter(user_id=self._user.id)

        if not orders:
            print(" У вас нет заказов")
        else:
            print(
                tabulate.tabulate(
                    # Это понимание списка, которое создает список списков, содержащих информацию о каждом заказе,
                    # сделанном текущим пользователем. Каждый внутренний список содержит идентификатор заказа, название
                    # заказанного продукта (полученное с помощью метода `Product.get()` с сохраненным в заказе
                    # идентификатором продукта), количество заказанных продуктов, а также дату и время заказа.
                    # Полученный список списков затем передается методу `tabulate.tabulate()`, чтобы создать
                    # отформатированную таблицу для отображения.
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
