import os
from typing import List

import requests

from import_helpers import get_file_in_input_data

WEBSITE_URL = "https://archive.org/download/stackexchange/"


# download_files downloads all fles to input data folder
def download_files(file_names: List[str], chunk_size=128) -> List[str]:
    files_on_disk = []
    for file in file_names:
        file_on_disk = get_file_in_input_data(file)
        files_on_disk.append(file_on_disk)

        r = requests.get(WEBSITE_URL + file)
        with open(file_on_disk, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
    return files_on_disk
