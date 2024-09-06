from models.category import Category
from models.category_db import CategoryDb
from repositories.category_repository import CategoryRepository
from unitofwork.unit_of_work import UnitOfWork


class CategoryService:
    """
    Service class for managing operations related to categories.

    This service acts as an intermediary between the controller and the
    repository layer, utilizing the Unit of Work pattern to ensure
    consistency in transactions.

    :param unit_of_work: The UnitOfWork instance used to manage database operations.
    :type unit_of_work: UnitOfWork
    """

    def __init__(self, unit_of_work: UnitOfWork):
        """
        Initializes the CategoryService with a UnitOfWork instance.

        :param unit_of_work: The UnitOfWork instance used for managing database operations.
        :type unit_of_work: UnitOfWork
        """

        self.__unit_of_work = unit_of_work

    def add_category(self, name: str) -> Category:
        """
        Adds a new category with the specified name.

        This method creates a new category in the database by using the
        Unit of Work pattern to ensure transactional integrity. It adds
        the new category to the repository and returns the business
        object representation of the category.

        :param name: The name of the category to add.
        :type name: str
        :return: A business object representing the newly added category.
        :rtype: Category
        :raises IntegrityError: If a category with the same name already exists
                                or any other integrity constraints are violated.
        :raises SQLAlchemyError: If any other database-related error occurs.
        """
        with self.__unit_of_work as uow:
            category_repository = uow.categories
            new_category = CategoryDb(name=name)
            category_repository.add(new_category)
            return Category(new_category.name)

    def get_category_by_name(self, name: str) -> Category:
        """
        Retrieves a category by its name.

        This method uses the Unit of Work to fetch the category from
        the repository within a transactional context. If the category is
        not found, the `ObjectNotFoundError` is raised by the repository and
        propagated up to this method.

        :param name: The name of the category to retrieve.
        :type name: str
        :return: The category business object if found.
        :rtype: Category
        :raises ObjectNotFoundError: If the category with the given name is not found in the repository.
        """

        with self.__unit_of_work as uow:
            category_repository: CategoryRepository = uow.categories
            category_database_model = category_repository.get_by_primary_key(name)
            return Category(category_database_model.name)
