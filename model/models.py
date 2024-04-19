from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Column, ForeignKey
from db.database import Base
from uuid import uuid4

class DbReview(Base):
    __tablename__= 'reviews'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    rating = Column(Integer)
    item = Column(String)
    comment =  Column(String)
    user = Column(String)
    creator = Column(String)
    modified_date = Column(String)
    created_date = Column(String)
    slug = Column(String)