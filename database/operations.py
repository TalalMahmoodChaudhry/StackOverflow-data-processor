import os
from typing import List

from sqlalchemy import Table, text
from sqlalchemy.dialects.sqlite import insert

from database.initialization import errors_table, engine

from constants import POSTGRES_DATABASE_ENV_VAR


# save_parsed_data saves the parsed contents of file to table
from import_helpers import get_sql_query_file


def save_parsed_data(db_table: Table, list_of_rows: List[dict]) -> None:
    stmt = insert(db_table).values(list_of_rows)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["id"],
    )
    engine.execute(stmt)


# save_errors_to_db saves all parsing errors to db
def save_errors_to_db(parsing_errors: List[dict]) -> None:
    if parsing_errors:
        stmt = insert(errors_table).values(parsing_errors)
        engine.execute(stmt)


# save_all_data_to_db saves the parsing data and errors to db
def save_all_data_to_db(table: Table, list_of_parsed_data: List[dict], parsing_errors: List[dict]) -> None:
    save_parsed_data(table, list_of_parsed_data)
    save_errors_to_db(parsing_errors)


def update_users_posts(connection, last_timestamp) -> None:
    with open(get_sql_query_file("update_posts.sql")) as f:
        query = f.read()
        query = query.format(last_timestamp=last_timestamp)
        connection.execute(query)


# POSTGRES and SQLite has different syntax. For this update different sql files used depending on db
def update_user_avg_monthly_comments(connection) -> None:
    if os.environ.get(POSTGRES_DATABASE_ENV_VAR):
        comments_sql = get_sql_query_file("average_comments_postgres.sql")
    else:
        comments_sql = get_sql_query_file("average_comments.sql")
    with open(comments_sql) as f:
        query = f.read()
        connection.execute(query)


# update_users_table updates the users' table with total posts and avg monthly comments from raw tables
def update_users_table(last_timestamp) -> None:
    with engine.begin() as connection:
        update_users_posts(connection, last_timestamp)

        update_user_avg_monthly_comments(connection)
