from sqlalchemy.orm import Session

from models.category_db import CategoryDb
from repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[CategoryDb]):
    def __init__(self, session: Session):
        super().__init__(session, CategoryDb)
