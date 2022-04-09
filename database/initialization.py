from sqlalchemy import MetaData, Table

from constants import ERRORS_TABLE_NAME, COMMENTS_TABLE_NAME, POSTS_TABLE_NAME, USERS_TABLE_NAME
from database.connection import engine
from database.models import Base

Base.metadata.create_all(bind=engine)

metadata = MetaData()
metadata.reflect(engine)

errors_table = Table(ERRORS_TABLE_NAME, metadata)
posts_table = Table(POSTS_TABLE_NAME, metadata)
users_table = Table(USERS_TABLE_NAME, metadata)
comments_table = Table(COMMENTS_TABLE_NAME, metadata)
