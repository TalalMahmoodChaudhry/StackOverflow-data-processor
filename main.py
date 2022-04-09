import argparse
import datetime
import os
import shutil
import xml.etree.ElementTree as ET
from typing import IO
import logging
from sqlalchemy import Table

from constants import BULK_IMPORT_LIMIT
from database.initialization import engine
from database.initialization import posts_table, comments_table, users_table
from database.operations import save_all_data_to_db, update_users_table
from download_stacks import download_files
from logging_handlers import initialize_logging
from schemas import users, posts, comments
from schemas.errors import get_error_from_xml_tree, is_error
from file_operations import unzip_files, pre_downloaded_data_folders


initialize_logging()
logger = logging.getLogger(os.path.basename(__file__))


# save_file_stream saves all rows in a stream to table in db
def save_file_stream(file_stream: IO, table: Table, func_get_data_from_xml_tree) -> None:
    # counter is used for bulk imports to db
    counter = 0

    data = []
    parsing_errors = []

    while True:

        # reading line by line to "simulate stream events"
        try:
            line = file_stream.readline()
        except Exception as e:
            error = get_error_from_xml_tree("Failed to Read line", str(e))
            parsing_errors.append(error.__dict__)
            continue

        # break if end of file
        if not line:
            save_all_data_to_db(table, data, parsing_errors)
            break

        # parse xml string. a more sophisticated parsing in production with better error handling
        # is probably better. E.g., by using regex which can extract all minimum required data even
        # if the xml format is invalid.
        try:
            tree = ET.fromstring(line)
        except ET.ParseError as e:
            if is_error(line):
                error = get_error_from_xml_tree(f"Failed to parse xml string: {line}", e.msg)
                parsing_errors.append(error.__dict__)
            continue

        # get users row according to defined schema
        try:
            row = func_get_data_from_xml_tree(tree)
        except ValueError as e:
            error = get_error_from_xml_tree(f"Schema definition failed for line {line}", str(e))
            parsing_errors.append(error.__dict__)
            continue

        # append data to list for bulk insert later
        data.append(row.__dict__)
        counter += 1

        # bulk insert to db
        if counter == BULK_IMPORT_LIMIT:
            save_all_data_to_db(table, data, parsing_errors)

            data = []
            parsing_errors = []
            counter = 0


# save_data_in_file_to_db reads the data in file and saves contents to db
def save_data_in_file_to_db(folder_name, file_name, table, func_get_data_from_xml_tree):
    with open(os.path.join(folder_name, file_name), errors="ignore") as f:
        save_file_stream(f, table, func_get_data_from_xml_tree)


parser = argparse.ArgumentParser()
parser.add_argument("--stacks", default=["german.meta.stackexchange.com.7z", "french.meta.stackexchange.com.7z"],
                    nargs="+", type=str, help="File names as shown on website. Example: german.meta.stackexchange.com.7z")
parser.add_argument("--download-data", action=argparse.BooleanOptionalAction,
                    help="Set to true if data not already downloaded and extracted. Default false.")
args = parser.parse_args()

if __name__ == "__main__":
    # Parse args
    files = args.stacks
    download_data = args.download_data

    # If data not already downloaded then download and extract
    if download_data:
        logger.info("Downloading all stacks")
        files = download_files(files)
        folders = unzip_files(files)
    else:
        folders = pre_downloaded_data_folders(files)

    # Loop over all folders to stream data from files and updates users table
    for folder in folders:
        logger.info(f"Parsing files in folder {folder}")

        # Get last record_insert_date_time
        sql_exec = engine.execute("select max(record_insert_date_time) from posts;")
        latest_record_timestamp = sql_exec.all()[0][0]
        latest_record_timestamp = latest_record_timestamp if latest_record_timestamp else datetime.datetime.utcnow()

        # read all relevant files and sav edata to db
        save_data_in_file_to_db(folder, "Users.xml", users_table, users.get_user_from_xml_tree)
        save_data_in_file_to_db(folder, "Posts.xml", posts_table, posts.get_post_from_xml_tree)
        save_data_in_file_to_db(folder, "Comments.xml", comments_table, comments.get_comment_from_xml_tree)

        logger.info("Update users table with new data")
        update_users_table(latest_record_timestamp)

        # cleanup
        if download_data:
            shutil.rmtree(folder)

    logger.info("Process finished. Shutting down")
