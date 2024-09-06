from abc import ABC
from typing import Generic, TypeVar, Type

from sqlalchemy.orm import Session

from exceptions.object_not_found_error import ObjectNotFoundError

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Base class for generic repository operations.

    This class provides basic CRUD (Create, Read, Update, Delete) operations
    for any SQLAlchemy model class.

    :param session: SQLAlchemy session used for database operations.
    :type session: Session
    :param model_class: Model class associated with the repository.
    :type model_class: Type[T]
    """

    def __init__(self, session: Session, model_class: Type[T]):
        """
        Initializes the repository with a database session and model class.

        :param session: SQLAlchemy session used to interact with the database.
        :type session: Session
        :param model_class: The SQLAlchemy model class this repository manages.
        :type model_class: Type[T]
        """

        self._session = session
        self._model_class = model_class

    def add(self, instance: T) -> None:
        """
        Adds an instance of the database model to the session.

        :param instance: The model instance to add to the session.
        :type instance: T
        """
        self._session.add(instance)

    def get_by_primary_key(self, primary_key: str | int) -> T:

        """
        Retrieves an instance of the database model by its primary key.

        :param primary_key: The primary key of the model instance to retrieve. Must be a string or an integer.
        :type primary_key: str | int
        :raises ObjectNotFoundError: If the model instance with the given primary key is not found.
        :returns: The instance of the model.
        :rtype: T
        """

        instance = self._session.get(self._model_class, primary_key)

        if not instance:
            raise ObjectNotFoundError(f"The {self._model_class.__name__} with primary key {primary_key} not found.")

        return instance

    def list(self) -> list[T]:
        """
        Retrieves all instances of the database model from the database.

        :returns: A list of all model instances.
        :rtype: list[T]
        """

        return self._session.query(self._model_class).all()

    def update_by_primary_key(self, primary_key, **kwargs) -> None:
        """
        Updates an instance of the database model by its primary key with provided attributes.

        :param primary_key: The primary key of the model instance to update.
        :type primary_key: Any
        :param kwargs: Key-value pairs of attributes to update on the model instance.
        :raises ObjectNotFoundError: If the model instance with the given primary key is not found.
        :raises AttributeError: If an invalid attribute is provided for the model.
        """

        instance = self._session.get(self._model_class, primary_key)

        if not instance:
            raise ObjectNotFoundError(f"The {self._model_class.__name__} with primary key {primary_key} not found.")

        for key, value in kwargs.items():
            if not hasattr(instance, key):
                raise AttributeError(f'{self._model_class.__name__} object has no attribute {key}.')
            setattr(instance, key, value)

        self._session.add(instance)

    def delete_by_primary_key(self, primary_key) -> None:
        """
        Deletes an instance of the database model by its primary key.

        :param primary_key: The primary key of the model instance to delete.
        :type primary_key: Any
        :raises ObjectNotFoundError: If the model instance with the given primary key is not found.
        """

        instance = self._session.get(self._model_class, primary_key)

        if not instance:
            raise ObjectNotFoundError(f"The {self._model_class.__name__} with primary key {primary_key} not found.")

        self._session.delete(instance)
