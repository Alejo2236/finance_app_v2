from abc import ABC
from typing import Generic, TypeVar, Type, Optional

from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    def __init__(self, session: Session, model_class: Type[T]):
        self.__session = session
        self.__model_class = model_class

    def add(self, instance: T) -> None:
        self.__session.add(instance)

    def get_by_primary_key(self, primary_key) -> Optional[T]:
        return self.__session.query(self.__model_class).get(primary_key)

    def list(self) -> list[T]:
        return self.__session.query(self.__model_class).all()

    def update_by_primary_key(self, primary_key, **kwargs) -> None:
        instance = self.__session.query(self.__model_class).get(primary_key)

        if not instance:
            raise ValueError(f'Object "{self.__model_class.__name__}" with primary key "{primary_key}" not found.')

        for key, value in kwargs.items():
            if not hasattr(instance, key):
                raise AttributeError(f'{self.__model_class.__name__} object has no attribute {key}.')
            setattr(instance, key, value)

        self.__session.add(instance)

    def delete_by_primary_key(self, primary_key) -> None:
        instance = self.__session.query(self.__model_class).get(primary_key)

        if not instance:
            raise ValueError(f'Object "{self.__model_class}" with primary key "{primary_key}" not found.')

        self.__session.delete(instance)
