from models.category import Category
from unitofwork.unit_of_work import UnitOfWork


class CategoryService:
    """
    Service class for managing operations related to categories.

    This service acts as an intermediary between the controller and the
    repository layer, utilizing the Unit of Work pattern to ensure
    consistency in transactions.

    :param unit_of_work: The UnitOfWork instance used to manage database operations.
    """

    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work = unit_of_work

    def get_category_by_name(self, name: str) -> Category:
        """
        Retrieves a category by its name.

        This method uses the Unit of Work to fetch the category from
        the repository within a transactional context. If any error occurs in the repository, the expection will be propagated

        :param name: The name of the category to retrieve.
        :type name: str
        :return: The category business object if found.
        :rtype: Category
        """
        with self.__unit_of_work as uow:
            category_repository = uow.categories
            category_database_model = category_repository.get_by_primary_key(name)
            return Category(category_database_model.name)
