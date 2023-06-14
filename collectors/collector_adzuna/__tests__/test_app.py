from unittest.mock import patch, Mock
from ..app import collector_adzuna
import json
import requests_mock
import pytest
import os
import shutil
import csv

dirpath = 'collector_adzuna/__tests__/csv'


@pytest.fixture(scope="session", autouse=True)
def create_csv():

    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

    generate_csv()

    yield

    shutil.rmtree(dirpath)


def generate_inputstream(path):
    """converts a local csv file and returns a mocked blob input stream containing that data"""
    with open(path, 'rb') as file:
        test_csv_data = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_csv_data

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_one_request_is_made_to_API_with_correctly_formatted_result(mock, create_csv):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1', json={"count": 227})

        test_input_stream = generate_inputstream("./collector_adzuna/__tests__/csv/test_one_skill.csv")

        result = collector_adzuna(test_input_stream)

        assert m.call_count == 1
        assert result == json.dumps({"AngularJS": 227})


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_multiple_requests_made_to_API_with_correctly_formatted_result(mock):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what=AngularJS', json={"count": 227})
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what=CSS', json={"count": 4608})

        test_input_stream = generate_inputstream("./collector_adzuna/__tests__/csv/test_skills.csv")

        result = collector_adzuna(test_input_stream)

        assert m.call_count == 2
        assert result == json.dumps({"AngularJS": 227, "CSS": 4608})


def test_error_raised_when_skills_csv_is_empty():
    test_input_stream = generate_inputstream("./collector_adzuna/__tests__/csv/test_skills_empty.csv")

    with pytest.raises(Exception) as error:
        collector_adzuna(test_input_stream)

    assert str(error.value) == 'List of skills is empty, CSV may be empty'


def generate_csv():
    """creates a series of CSVs containing data needed for tests"""

    os.mkdir(f'{dirpath}')

    with open(f'{dirpath}/test_one_skill.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        csvwriter.writerow(['', 'course_skills'])
        csvwriter.writerow(['0', 'AngularJS'])

    with open(f'{dirpath}/test_skills_empty.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')

    with open(f'{dirpath}/test_skills.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        csvwriter.writerow(['', 'course_skills'])
        csvwriter.writerow(['0', 'AngularJS'])
        csvwriter.writerow(['1', 'CSS'])