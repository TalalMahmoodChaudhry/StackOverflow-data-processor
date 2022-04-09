import datetime

import file_operations

import xml.etree.ElementTree as ET

from constants import DATETIME_FORMAT


def test_pre_downloaded_data_folders():
    files = ["german.stackexchange.com.7z", "french.stackexchange.com.7z"]
    folders = file_operations.pre_downloaded_data_folders(files)

    assert len(folders) == 2


def test_get_safe_datetime_item_from_tree():
    datetime_str = "2011-08-17T18:34:28.120"
    datetime_obj = datetime.datetime.strptime(datetime_str, DATETIME_FORMAT)

    sample_xml_string = f'<row Id="-1" Reputation="1" CreationDate="{datetime_str}" AccountId="-1" />'
    tree = ET.fromstring(sample_xml_string)

    element = file_operations.get_safe_datetime_item_from_tree(tree, "CreationDate")
    assert element == datetime_obj
