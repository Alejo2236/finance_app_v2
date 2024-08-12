from typing import Callable

from sqlalchemy.orm import Session

from repositories.category_repository import CategoryRepository


class UnitOfWork:

    def __init__(self, session_factory: Callable[[], Session]):
        self.__session_factory = session_factory
        self.__repositories = {}

    def __enter__(self):
        self.__session = self.__session_factory()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.__rollback()
        else:
            self.__commit()
        self.__repositories.clear()
        self.__session.close()

    def __commit(self):
        self.__session.commit()

    def __rollback(self):
        self.__session.rollback()

    @property
    def categories(self) -> CategoryRepository:
        if 'categories' not in self.__repositories:
            self.__repositories['categories'] = CategoryRepository(self.__session)
        return self.__repositories['categories']
