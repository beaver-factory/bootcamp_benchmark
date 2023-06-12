from ..app import process_adzuna_data
import pytest
import os
import shutil
import json
from unittest.mock import Mock, patch
import csv
import io

dirpath = 'processor_adzuna/__tests__/json'


@pytest.fixture(scope="session", autouse=True)
def create_json():

    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

    generate_json()

    yield

    shutil.rmtree(dirpath)


def test_processor_returns_a_stringIO():
    test_input = generate_inputstream(f"{dirpath}/test_skills.json")
    result = process_adzuna_data(test_input)
    assert type(result) == io.StringIO


def test_processor_creates_csv_with_correct_headers_and_data():
    test_input = generate_inputstream(f"{dirpath}/test_skills.json")
    result = process_adzuna_data(test_input)

    csv_rows = convert_csv_to_list(result)

    csv_headers = csv_rows[0]
    csv_content = csv_rows[1:]

    assert csv_headers == ['skill', 'number_of_jobs']
    for row in csv_content:
        assert type(row[0]) is str
        assert type(int(row[1])) is int
    assert csv_content[0][0] == 'AngularJS'
    assert csv_content[0][1] == '200'


def test_raises_exception_when_json_is_empty():
    test_input = generate_inputstream(f"{dirpath}/empty_skills.json")

    with pytest.raises(Exception) as err:
        result = process_adzuna_data(test_input)

    assert str(err.value) == 'Adzuna raw json is empty'


def test_raises_exception_when_skill_count_is_wrong_data_type():
    test_input = generate_inputstream(f"{dirpath}/incorrect_data_type_for_skill_count.json")

    with pytest.raises(Exception) as err:
        process_adzuna_data(test_input)

    assert str(err.value) == 'At least one of the skills count values is not an integer'


def generate_inputstream(path):
    """converts a local csv file and returns a mocked blob input stream containing that data"""
    with open(path, 'rb') as file:
        test_json_data = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_json_data

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream


def generate_json():
    """creates a series of CSVs containing data needed for tests"""

    os.mkdir(f'{dirpath}')

    with open(f'{dirpath}/test_skills.json', 'w') as file:
        file.write(json.dumps({'AngularJS': 200, 'CSS': 300, 'HTML': 400}))

    with open(f'{dirpath}/empty_skills.json', 'w') as file:
        file.write(json.dumps({}))

    with open(f"{dirpath}/incorrect_data_type_for_skill_count.json", 'w') as file:
        file.write(json.dumps({'AngularJS': '200'}))


def convert_csv_to_list(csv_as_stringIO):
    csvfile = csv_as_stringIO.getvalue()
    csv_reader = csv.reader(csvfile.split('\n'), delimiter=',')
    csv_rows = []
    for row in csv_reader:
        if len(row) > 0:
            csv_rows.append(row)

    return csv_rows
