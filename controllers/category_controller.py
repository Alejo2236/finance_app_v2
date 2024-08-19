from models.category import Category
from services.category_service import CategoryService


class CategoryController:
    """
    Controller class for managing interactions related to categories.

    This controller serves as an intermediary between the user interface (UI)
    and the service layer, facilitating user requests and managing responses,
    including error handling.

    :param category_service: The service used to manage category-related operations.
    :type category_service: CategoryService
    """

    def __init__(self, category_service: CategoryService):
        """
        Initializes the CategoryController with a CategoryService instance.

        :param category_service: The service used to perform category operations.
        :type category_service: CategoryService
        """

        self.__category_service = CategoryService

    def get_category_by_name(self, name: str) -> Category:
        """
        Retrieves a category by its name.

        This method calls the CategoryService to fetch a category based on the
        provided name. If the category is not found, an ´ObjectNotFoundError´
        will be propagated to the view for handling.

        :param name: The name of the category to retrieve.
        :type name: str
        :return: The category business object if found.
        :rtype: Category
        :raises ObjectNotFoundError: If the category with the given name is not found.
        """

        return self.__category_service.get_category_by_name(name)
