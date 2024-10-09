from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=True)
    published_date = Column(TIMESTAMP, nullable=False)
    source_url = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=True)
