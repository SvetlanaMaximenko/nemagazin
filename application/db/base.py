from sqlalchemy import create_engine, select, exc, update as sqlalchemy_update
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class SessionManager:

    __instance = None

    def __init__(self):
        if not SessionManager.__instance:
            print(" __init__ method called..")
            self._engine = None
            self._session = None
        else:
            print("Instance already created:", self.get_instance())

    def init_engine(self, dsn: str):
        """
        Эта функция инициализирует механизм базы данных и сеанс, используя заданный DSN.

        :param dsn: dsn означает «Имя источника данных» и представляет собой строку, содержащую информацию,
         необходимую для подключения к базе данных. Обычно он включает тип базы данных, хост, порт, имя базы данных
         и учетные данные для аутентификации
        """
        self._engine = create_engine(dsn)
        self._session = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = SessionManager()
        return cls.__instance

    def __call__(self, *args, **kwargs):
        return self._session(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(self._session, item)

    def create_tables(self):
        """
        Метод создает таблицы в базе данных.
        """
        BaseModel.metadata.create_all(bind=self._engine)


session = SessionManager()


class BaseModel(DeclarativeBase):
    """
    Приведенный выше класс предоставляет методы для создания, обновления, фильтрации и извлечения экземпляров модели
    SQLAlchemy из базы данных.
    """

    @classmethod
    def get(cls, **kwargs):
        """
        Эта функция извлекает один объект из таблицы базы данных на основе предоставленных аргументов ключевого слова.

        :param cls: Параметр cls относится к объекту класса, в котором определен этот метод.
         Он используется для доступа к атрибутам и методам класса
        :return: Метод `get` возвращает один экземпляр класса модели SQLAlchemy, который соответствует предоставленным
         аргументам ключевого слова (`kwargs`). Если соответствующий экземпляр не найден, он возвращает «None».
        """

        params = [getattr(cls, key) == val for key, val in kwargs.items()]
        query = select(cls).where(*params)

        try:
            with session() as conn:
                results = conn.execute(query)
                (res,) = results.one()
                return res
        except exc.NoResultFound:
            return None

    @classmethod
    def create(cls, **kwargs):
        """
        Эта функция создает новый объект данного класса с предоставленными аргументами ключевого слова и сохраняет его в
        базе данных с помощью сеанса.

        :param cls: Параметр cls относится к классу, в котором определен метод create. Он используется для создания
         экземпляра этого класса
        :return: Метод create возвращает объект, который был создан и добавлен в базу данных.
        """
        obj = cls(**kwargs)
        with session() as conn:
            conn.add(obj)
            conn.commit()
        return obj

    def update(self, **kwargs) -> None:
        """
        Эта функция обновляет атрибуты объекта в базе данных с помощью SQLAlchemy.
        """
        with session() as conn:
            conn.execute(
                sqlalchemy_update(self.__class__)
                .where(self.__class__.id == self.id)
                .values(**kwargs)
            )
            conn.commit()

    @classmethod
    def filter(cls, **kwargs):
        """
        Эта функция фильтрует модель SQLAlchemy на основе заданных аргументов ключевого слова и
        возвращает соответствующие результаты.

        :param cls: Параметр cls является ссылкой на класс. Он используется для создания запроса SQLAlchemy
         для фильтрации экземпляров этого класса на основе предоставленных аргументов ключевого слова.
        :return: Метод filter возвращает список объектов, соответствующих критериям фильтрации,
         указанным в словаре kwargs. Если объекты не найдены, возвращается пустой список.
        """
        params = [getattr(cls, key) == val for key, val in kwargs.items()]
        query = select(cls).where(*params)
        try:
            with session() as conn:
                results = conn.execute(query)
                return results.scalars().all()
        except exc.NoResultFound:
            return []

    @classmethod
    def all(cls):
        """
        Эта функция возвращает все экземпляры класса SQLAlchemy из базы данных.

        Функция `select(cls)` используется для генерации оператора SQL SELECT для запроса всех строк из таблицы,
        представленной классом модели `cls`.

        Метод `results.scalars()` возвращает генератор, который выдает каждую строку результата запроса в виде
        скалярного значения, а метод `all()` преобразует этот генератор в список скалярных значений.

        :param cls: ссылка на объект класса. Класс модели SQLAlchemy представляет таблицу базы данных.
        :return: Метод all() возвращает список всех экземпляров класса cls, существующих в базе данных.
        """
        with session() as conn:
            results = conn.execute(select(cls))
            return results.scalars().all()
