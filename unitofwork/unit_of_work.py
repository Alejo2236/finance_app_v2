from typing import Callable

from sqlalchemy.orm import Session

from repositories.category_repository import CategoryRepository


class UnitOfWork:
    """
    A unit of work implementation that manages database transactions
    using a session factory and provides access to repositories.

    This class ensures that all operations within a single unit of work
    are atomic, meaning that either all succeed, or all fail and are rolled back.

    :param session_factory: A callable that returns a new SQLAlchemy session when invoked.
    """

    def __init__(self, session_factory: Callable[[], Session]):
        """
        Initializes the unit of work with a session factory.

        :param session_factory: A function that returns a new SQLAlchemy session.
        """

        self.__session_factory = session_factory
        self.__repositories = {}

    def __enter__(self):
        """
        Enters the context of the unit of work, initializing the session.

        :return: The unit of work instance.
        """

        self.__session = self.__session_factory()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the context of the unit of work, committing the transaction
        if there were no exceptions, or rolling back if any exception occurred.

        :param exc_type: The exception type if an exception was raised.
        :param exc_value: The exception instance if an exception was raised.
        :param traceback: The traceback object associated with the exception.
        """

        if exc_type is not None:
            self.__rollback()
        else:
            self.__commit()
        self.__repositories.clear()
        self.__session.close()

    def __commit(self):
        """Commits the current transaction."""

        self.__session.commit()

    def __rollback(self):
        """Rolls back the current transaction."""

        self.__session.rollback()

    @property
    def categories(self) -> CategoryRepository:
        """
        Lazily loads and returns the category repository.

        :return: An instance of CategoryRepository tied to the current session.
        """
        if 'categories' not in self.__repositories:
            self.__repositories['categories'] = CategoryRepository(self.__session)
        return self.__repositories['categories']

    # TODO: create properties for new repositories
