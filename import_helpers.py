import pkg_resources

INPUT_FOLDER = "input_data"


def get_file_in_input_data(file: str) -> str:
    return pkg_resources.resource_filename(INPUT_FOLDER, file)


def get_sql_query_file(file: str) -> str:
    return pkg_resources.resource_filename("database", f"sql_queries/{file}")
