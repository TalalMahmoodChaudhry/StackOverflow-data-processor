from sqlalchemy import Column, Integer, TEXT, TIMESTAMP, func, String, NUMERIC

from constants import ERRORS_TABLE_NAME, COMMENTS_TABLE_NAME, POSTS_TABLE_NAME, USERS_TABLE_NAME
from database.connection import Base


class ErrorsTable(Base):
    __tablename__ = ERRORS_TABLE_NAME

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    text = Column(TEXT)
    error_message = Column(TEXT)
    record_insert_date_time = Column(TIMESTAMP, server_default=func.now(), index=True)


class RawCommentsTable(Base):
    __tablename__ = COMMENTS_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer)
    score = Column(Integer)
    text = Column(TEXT)
    creation_date = Column(TIMESTAMP)
    # Same argument as in RawPosts
    user_id = Column(Integer, index=True)
    record_insert_date_time = Column(TIMESTAMP)


class RawPostsTable(Base):
    __tablename__ = POSTS_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    post_type_id = Column(Integer)
    parent_id = Column(Integer)
    acceptance_answer_id = Column(Integer)
    creation_date = Column(TIMESTAMP)
    score = Column(Integer)
    view_count = Column(Integer)
    body = Column(TEXT)
    # Foreign key could be set here to the id of RawUserTable however it is possible
    # that stream data coming in is unordered in production. For this task I could control
    # this, but I have made the assumption it may be unordered.
    owner_user_id = Column(Integer, index=True)
    last_editor_display_name = Column(String)
    last_edit_date = Column(TIMESTAMP, nullable=True)
    last_activity_date = Column(TIMESTAMP, nullable=True)
    community_owned_date = Column(TIMESTAMP, nullable=True)
    closed_date = Column(String)
    title = Column(String)
    tags = Column(String)
    answer_count = Column(Integer)
    comment_count = Column(Integer)
    favorite_count = Column(Integer)
    record_insert_date_time = Column(TIMESTAMP, index=True)


class Users(Base):
    __tablename__ = USERS_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    display_name = Column(String)
    reputation = Column(Integer)
    creation_date = Column(TIMESTAMP)
    last_access_date = Column(TIMESTAMP)
    website_url = Column(String)
    location = Column(String)
    about_me = Column(TEXT)
    views = Column(Integer)
    up_votes = Column(Integer)
    down_votes = Column(Integer)
    total_posts = Column(Integer)
    avg_monthly_comments = Column(NUMERIC)
