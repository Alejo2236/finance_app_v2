from typing import Callable

from sqlalchemy.orm import Session

from repositories.category_repository import CategoryRepository


class UnitOfWork:
    """
    A unit of work implementation that manages database transactions
    using a session factory and provides access to repositories.

    This class ensures that all operations within a single unit of work
    are atomic, meaning that either all succeed, or all fail and are rolled back.
    It uses a context manager interface (i.e., a `with' statement) to manage
    the session lifecycle and automatically handle commit and rollback operations.

    :param session_factory: A callable that returns a new SQLAlchemy session when invoked.
    :type session_factory: Callable[[], Session]
    """

    def __init__(self, session_factory: Callable[[], Session]):
        """
        Initializes the unit of work with a session factory.

        :param session_factory: A function that returns a new SQLAlchemy session.
        :type session_factory: Callable[[], Session]
        """

        self.__session_factory = session_factory
        self.__repositories = {}

    def __enter__(self):
        """
        Enters the context of the unit of work, initializing the session.

        This method is called at the start of a `with` block and sets up
        a new session using the session factory provided during initialization.

        :return: The unit of work instance.
        :rtype: UnitOfWork
        """

        self.__session = self.__session_factory()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the context of the unit of work, committing the transaction
        if there were no exceptions, or rolling back if any exception occurred.

        If an exception is raised during the operations within the `with` block,
        the transaction is rolled back to ensure data consistency.

        :param exc_type: The exception type if an exception was raised.
        :type exc_type: type
        :param exc_value: The exception instance if an exception was raised.
        :type exc_value: Exception
        :param traceback: The traceback object associated with the exception.
        :type traceback: traceback
        """

        if exc_type is not None:
            self.__rollback()
        else:
            self.__commit()
        self.__repositories.clear()
        self.__session.close()

    def __commit(self) -> None:
        """
        Commits the current transaction.

        This method is called internally to commit the changes made during
        the unit of work. Any errors during the commit process will result
        in an exception that should be handled by the caller.
        """

        self.__session.commit()

    def __rollback(self) -> None:
        """
        Rolls back the current transaction.

        This method is called internally if an exception occurs during the unit of work,
        ensuring that no partial changes are committed to the database.
        """

        self.__session.rollback()

    @property
    def categories(self) -> CategoryRepository:
        """
        Lazily loads and returns the category repository.

        The repository is instantiated on first access and tied to the current
        session. This approach allows for efficient resource usage and ensures
        that each repository shares the same transactional context.

        :return: An instance of CategoryRepository tied to the current session.
        :rtype: CategoryRepository
        """
        if 'categories' not in self.__repositories:
            self.__repositories['categories'] = CategoryRepository(self.__session)
        return self.__repositories['categories']

    # TODO: create properties for new repositories
