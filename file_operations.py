import errno
import os
from datetime import datetime
from typing import List

import py7zr

from constants import DATETIME_FORMAT


# get_safe_datetime_item_from_tree returns the datetime and doesn't throw exception in element not in tree
from import_helpers import get_file_in_input_data


def get_safe_datetime_item_from_tree(tree, element) -> datetime:
    item = tree.get(element)
    if item:
        try:
            item = datetime.strptime(item, DATETIME_FORMAT)
        except ValueError:
            pass
    return item


# unzip_file unzips the 7z to input data folder and returns the folder name
def unzip_file(name: str) -> str:
    with py7zr.SevenZipFile(name, mode='r') as z:
        folder = name[:-3]
        z.extractall(path=folder)
    silent_remove(name)
    return folder


# unzip_files unzips multiple files to input data folder and returns the folder names
def unzip_files(names: List[str]) -> List[str]:
    folders = []
    for file in names:
        folders.append(unzip_file(file))
    return folders


# pre_downloaded_data_folders returns the folders with data already present (german and french stacks0
def pre_downloaded_data_folders(files: List[str]) -> List[str]:
    folders = []
    for file in files:
        folders.append(get_file_in_input_data(file[:-3]))
    return folders


def silent_remove(filename: str) -> None:
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
