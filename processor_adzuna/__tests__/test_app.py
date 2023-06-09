from ..app import process_adzuna_data
import pytest
import os
import shutil
import json
from unittest.mock import Mock, patch
import csv

dirpath = 'processor_adzuna/__tests__/json'


def test_app():
    test_input = generate_inputstream(f"{dirpath}/one_skill.json")
    test_csv = process_adzuna_data(test_input)
    test_csv.close()

    with open('processed_skill_count.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        csv_rows = []
        for row in csv_reader:
            csv_rows.append(row)

        csv_headers = csv_rows[0]
        csv_content = csv_rows[1:]

        assert csv_headers == ['skill', 'number_of_jobs']
        for row in csv_content:
            assert type(row[0]) is str
            assert type(int(row[1])) is int


@pytest.fixture(scope="session", autouse=True)
def create_json():

    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

    generate_json()

    yield

    shutil.rmtree(dirpath)


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

    with open(f'{dirpath}/one_skill.json', 'w') as file:
        file.write(json.dumps({'AngularJS': 200}))
