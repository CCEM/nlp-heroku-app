from sqlalchemy import (
    Column,
    Index,
    Text,
    PickleType
)

from .meta import Base


class SubReddit(Base):
    __tablename__ = 'SubReddit'
    name = Column(Text, primary_key=True)
    scores = Column(PickleType)


Index('name', SubReddit.name, unique=True, mysql_length=255)
