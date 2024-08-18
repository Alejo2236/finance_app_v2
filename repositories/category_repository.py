from sqlalchemy.orm import Session

from models.category_db import CategoryDb
from repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[CategoryDb]):
    """
    Repository for handling operations related to the Category model.

    Inherits the base CRUD operations from BaseRepository.
    """

    def __init__(self, session: Session):
        """
        Initializes the CategoryRepository with a specific session.

        :param session: SQLAlchemy session used to interact with the database.
        :type session: Session
        """

        super().__init__(session, CategoryDb)
