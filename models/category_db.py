from sqlalchemy import Column, String

from models.model_base import Base


class CategoryDb(Base):
    __tablename__ = 'categories'

    name = Column(String, primary_key=True)
