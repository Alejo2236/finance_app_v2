import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.model_base import Base
from services.category_service import CategoryService
from unitofwork.unit_of_work import UnitOfWork


class TestCategoryService(unittest.TestCase):
    SessionMaker = None
    engine = None

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test database and create the schema."""
        cls.engine = create_engine('sqlite:///:memory:')
        cls.SessionMaker = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.unit_of_work = UnitOfWork(cls.SessionMaker)

    def test_add_valid_category(self):
        TEST_NAME = "Test Category"
        category_service = CategoryService(self.unit_of_work)
        category_service.add_category(TEST_NAME)
        retrieved_category = category_service.get_category_by_name(TEST_NAME)
        self.assertIsNotNone(retrieved_category)
        self.assertEqual(retrieved_category.name, TEST_NAME)


