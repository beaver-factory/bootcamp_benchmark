from unittest.mock import patch, Mock
from ..app import collector_adzuna, create_keyword_query
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


test_dict = {'Express': ['express', 'expressjs', 'express.js'], 'CSS': ['css', 'css3.0'], 'HTML': ['html', 'html5'], 'React': ['react', 'react.js', 'reactjs'], 'Java': ['java'], 'Asana': ['asana'], 'Data Engineering': ['data engineering'], 'GCP': ['gcp', 'google cloud', 'google cloud platform'], 'C#': ['c#']}


@pytest.fixture(scope="session", autouse=True)
def create_skills_json():

    path = 'collector_adzuna/__tests__/skills_dict.json'

    if os.path.isfile(path):
        os.remove(path)

    with open(f'{path}', 'w') as file:
        file.write(json.dumps(test_dict))

    yield

    os.remove(path)


def generate_inputstream(path):
    """converts a local csv file and returns a mocked blob input stream containing that data"""
    with open(path, 'rb') as file:
        test_csv_data = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_csv_data

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream


def generate_skills_dict_input_stream():
    """converts a local csv file and returns a mocked blob input stream containing that data"""
    with open('collector_adzuna/__tests__/skills_dict.json', 'rb') as file:
        test_skills_dict_json = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_skills_dict_json

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_one_request_is_made_to_API_with_correctly_formatted_result(mock, create_csv):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 227})

        test_csv_input_stream = generate_inputstream(
            "./collector_adzuna/__tests__/csv/test_one_skill.csv")

        test_json_input_stream = generate_skills_dict_input_stream()

        result = collector_adzuna(test_csv_input_stream, test_json_input_stream)

        assert m.call_count == 1
        assert result == json.dumps({"HTML": 227})


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_multiple_requests_made_to_API_with_correctly_formatted_result(mock):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what=java&title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 227})
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what=asana&title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 4608})

        test_input_stream = generate_inputstream(
            "./collector_adzuna/__tests__/csv/test_skills.csv")

        test_json_input_stream = generate_skills_dict_input_stream()

        result = collector_adzuna(test_input_stream, test_json_input_stream)

        assert m.call_count == 2
        assert result == json.dumps({"java": 227, "asana": 4608})


def test_error_raised_when_skills_csv_is_empty():
    test_input_stream = generate_inputstream(
        "./collector_adzuna/__tests__/csv/test_skills_empty.csv")

    test_json_input_stream = generate_skills_dict_input_stream()

    with pytest.raises(Exception) as error:
        collector_adzuna(test_input_stream, test_json_input_stream)

    assert str(error.value) == 'List of skills is empty, CSV may be empty'


def test_create_keyword_query_returns_same_keyword_when_no_processing_needed():
    keyword = "java"
    result = create_keyword_query(keyword, test_dict)
    expected = "what=java"

    assert result == expected


def test_create_keyword_query_returns_variants_of_skill_when_matches_key_in_skills_dict():
    keyword = "React"
    result = create_keyword_query(keyword, test_dict)
    expected = "what_or=react%20react.js%20reactjs"

    assert result == expected


def test_create_keyword_query_returns_variants_of_skill_when_matches_value_in_skills_dict():
    keyword = "React.js"
    result = create_keyword_query(keyword, test_dict)
    expected = "what_or=react%20react.js%20reactjs"

    assert result == expected


def test_create_keyword_query_returns_a_what_phrase_when_multi_word_passed_in():
    keyword = 'data engineering'
    result = create_keyword_query(keyword, test_dict)
    expected = 'what_phrase=data%20engineering'

    assert result == expected


def test_create_keyword_query_returns_what_and_key_when_synonynms_contains_spaces():
    keyword = 'google cloud platform'
    result = create_keyword_query(keyword, test_dict)
    expected = 'what=gcp'

    assert result == expected


def test_create_keyword_query_returns_encoded_chars():
    keyword = 'C#'
    result = create_keyword_query(keyword, test_dict)
    expected = 'what=c%23'

    assert result == expected


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_api_called_with_expected_url_when_synonyms_present(mock):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what_or=react%20react.js%20reactjs&title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 227})
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what_phrase=data%20engineering&title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 4608})

        test_input_stream = generate_inputstream(
            "./collector_adzuna/__tests__/csv/test_skills_with_synonyms.csv")

        test_json_input_stream = generate_skills_dict_input_stream()

        result = collector_adzuna(test_input_stream, test_json_input_stream)

        assert m.call_count == 2
        assert result == json.dumps({"react": 227, "data engineering": 4608})


def generate_csv():
    """Creates a series of CSVs containing data needed for tests"""

    os.mkdir(f'{dirpath}')

    with open(f'{dirpath}/test_one_skill.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        csvwriter.writerow(['', 'course_skills'])
        csvwriter.writerow(['0', 'HTML'])

    with open(f'{dirpath}/test_skills_empty.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')

    with open(f'{dirpath}/test_skills.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        csvwriter.writerow(['', 'course_skills'])
        csvwriter.writerow(['0', 'java'])
        csvwriter.writerow(['1', 'asana'])

    with open(f'{dirpath}/test_skills_with_synonyms.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        csvwriter.writerow(['', 'course_skills'])
        csvwriter.writerow(['0', 'react'])
        csvwriter.writerow(['1', 'data engineering'])
