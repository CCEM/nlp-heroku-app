from sqlalchemy import (
    Column,
    Index,
    Text,
    Float,
    DateTime,
    Integer
)

from .meta import Base


class SubReddit(Base):
    __tablename__ = 'SubReddit'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    mean = Column(Float)
    median = Column(Float)
    date = Column(DateTime)


Index('id', SubReddit.id, unique=True, mysql_length=255)
