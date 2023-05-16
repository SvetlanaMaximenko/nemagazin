from application.db import session
from application.menu import UserMenu
from application.service import ShopService, User
from application.storage import MemoryStorage


if __name__ == "__main__":
    session.init_engine("postgresql://sveta:0310@localhost:5432/sv")
    session.create_tables()

    memory_storage = MemoryStorage()
    service = ShopService(storage=memory_storage)

    with open('user_login.txt', 'r') as file:
        data = file.read()
        if data is None:
            menu = UserMenu(storage=memory_storage)
        else:
            user = User.get(username=data)
            service._login_user(user)

    menu = UserMenu(storage=memory_storage)

    menu.add_menu_category(
        name="Войти",
        callback=service.login,
        login_required=1,
    )
    menu.add_menu_category(
        name="Зарегистрироваться",
        callback=service.register,
        login_required=1,
    )
    menu.add_menu_category(
        name="Товары",
        callback=service.display_products,
        login_required=0,
    )
    menu.add_menu_category(
        name="Выйти из программы",
        callback=service.exit_prog,
        login_required=0,
    )
    menu.add_menu_category(
        name="Тикет",
        callback=service.submit_ticket,
        login_required=2,
    )
    menu.add_menu_category(
        name="Купить",
        callback=service.buy_product,
        login_required=2,
    )
    menu.add_menu_category(
        name="Профиль",
        callback=service.profile,
        login_required=2,
    )
    menu.add_menu_category(
        name="Сменить пользователя",
        callback=service.change_profile,
        login_required=2,
    )
    while True:
        menu.display_categories()
        menu.handler()

