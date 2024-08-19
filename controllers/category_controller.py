from exceptions.object_not_found_error import ObjectNotFoundError
from models.category import Category
from services.category_service import CategoryService


class CategoryController:
    def __init__(self, category_service: CategoryService):
        self.__category_service = CategoryService

    def get_category_by_name(self, name: str) -> Category:
        try:
            return self.__category_service.get_category_by_name(name)
        except ObjectNotFoundError:
            # TODO create a dialog or show in the view the error
            print("there was an error")