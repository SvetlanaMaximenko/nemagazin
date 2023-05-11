from application.db import session
from application.menu import UserMenu
from application.service import ShopService
from application.storage import MemoryStorage


if __name__ == "__main__":
    session.init_engine("sqlite:///db.sqlite3")
    session.create_tables()

    memory_storage = MemoryStorage()

    menu = UserMenu(storage=memory_storage)
    service = ShopService(storage=memory_storage)

    menu.add_menu_category(
        name="Войти",
        callback=service.login,
        login_required=False,
    )
    menu.add_menu_category(
        name="Зарегистрироваться",
        callback=service.register,
        login_required=False,
    )
    menu.add_menu_category(
        name="Тикет",
        callback=service.submit_ticket,
        login_required=True,
    )
    menu.add_menu_category(
        name="Купить",
        callback=service.buy_product,
        login_required=True,
    )
    menu.add_menu_category(
        name="Профиль",
        callback=service.profile,
        login_required=True,
    )
    menu.add_menu_category(
        name="Товары",
        callback=service.display_products,
        login_required=False,
    )

    while True:
        menu.display_categories()
        menu.handler()
