from unitofwork.unit_of_work import UnitOfWork


class CategoryService:
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work = unit_of_work

    def get_category_by_name(self, name: str):
        with self.__unit_of_work as uow:
            category_repository = uow.categories
            category_repository.get_by_primary_key(name)
