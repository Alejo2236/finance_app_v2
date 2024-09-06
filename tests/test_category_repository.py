import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from exceptions.object_not_found_error import ObjectNotFoundError
from models.category_db import CategoryDb
from models.model_base import Base
from repositories.category_repository import CategoryRepository


class TestCategoryRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test database and create the schema."""
        cls.engine = create_engine('sqlite:///:memory:')
        cls.SessionMaker = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)

    def setUp(self) -> None:
        """Set up a new session for each test."""
        self.session = self.SessionMaker()
        self.repository = CategoryRepository(self.session)

    def tearDown(self) -> None:
        """Rollback any changes and close the session."""
        self.session.rollback()
        self.session.close()

    def test_add_category(self) -> None:
        """Test adding a new category"""
        category = CategoryDb(name="Test Category")
        self.repository.add(category)
        self.session.flush()
        retrieved_category = self.repository.get_by_primary_key(category.name)
        self.assertIsNotNone(retrieved_category)
        self.assertEqual(retrieved_category.name, "Test Category")

    def test_get_category_not_found(self):
        """Test retrieving a category that does not exist."""
        with self.assertRaises(ObjectNotFoundError):
            self.repository.get_by_primary_key("This category doesn't exists")

    def test_update_category(self):
        """Test updating an existing category."""
        category = CategoryDb(name="Original Name")
        self.repository.add(category)
        self.session.flush()

        self.repository.update_by_primary_key(category.name, name="Updated Name")
        self.session.flush()

        updated_category = self.repository.get_by_primary_key(category.name)
        self.assertEqual(updated_category.name, "Updated Name")

    def test_delete_category(self):
        """Test deleting an existing category."""
        category = CategoryDb(name="To Be Deleted")
        self.repository.add(category)
        self.session.flush()

        self.repository.delete_by_primary_key(category.name)
        self.session.flush()
        with self.assertRaises(ObjectNotFoundError):
            self.repository.get_by_primary_key(category.name)
