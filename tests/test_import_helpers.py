import import_helpers


def test_get_file_in_input_data():
    file = import_helpers.get_file_in_input_data("test.txt")
    assert file is not None


def test_get_sql_query_file():
    file = import_helpers.get_sql_query_file("test.sql")
    assert file is not None
