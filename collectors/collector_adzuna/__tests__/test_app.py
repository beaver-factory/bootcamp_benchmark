from unittest.mock import patch, Mock
from ..app import collector_adzuna, create_keyword_query
import json
import requests_mock
import pytest
import os
import shutil

dirpath = 'collector_adzuna/__tests__/json'


test_dict = {'Express': ['express', 'expressjs', 'express.js'], 'CSS': ['css', 'css3.0'], 'HTML': ['html', 'html5'], 'React': ['react', 'react.js', 'reactjs'], 'Java': ['java'], 'Asana': ['asana'], 'Data Engineering': ['data engineering'], 'GCP': ['gcp', 'google cloud', 'google cloud platform'], 'C#': ['c#']}


@pytest.fixture(scope="session", autouse=True)
def create_skills_json():

    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

    generate_test_jsons()

    yield

    shutil.rmtree(dirpath)


def generate_skills_dict_input_stream(path):
    """converts a local json file and returns a mocked blob input stream containing that data"""
    with open(path, 'rb') as file:
        test_skills_dict_json = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_skills_dict_json

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream


def generate_test_jsons():

    os.mkdir(dirpath)

    with open(dirpath + '/single_skills_dict.json', 'w') as file:
        file.write(json.dumps({'Java': ['java']}))

    with open(dirpath + '/no_synonyms_skills_dict.json', 'w') as file:
        file.write(json.dumps({'Java': ['java'], 'Asana': ['asana']}))

    with open(dirpath + '/empty_skills_dict.json', 'w') as file:
        file.write(json.dumps({}))

    with open(dirpath + '/phrases_in_skills_dict.json', 'w') as file:
        file.write(json.dumps({'Data Engineering': ['data engineering']}))

    with open(dirpath + '/single_word_synonyms_in_skills_dict.json', 'w') as file:
        file.write(json.dumps({'React': ['react', 'react.js', 'reactjs']}))

    with open(dirpath + '/multi_word_synonyms_in_skills_dict.json', 'w') as file:
        file.write(json.dumps({'GCP': ["gcp", "google cloud", "google cloud platform"]}))


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_one_request_is_made_to_API_with_correctly_formatted_result(mock):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?title_only=junior&location0=UK&category=it-jobs&content-type=application/json&what=java',
              json={"count": 227})

        test_json_input_stream = generate_skills_dict_input_stream(dirpath + '/single_skills_dict.json')

        result = collector_adzuna(test_json_input_stream)

        assert m.call_count == 1
        assert result == json.dumps({"Java": 227})


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_multiple_requests_made_to_API_with_correctly_formatted_result(mock):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what=java&title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 227})
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what=asana&title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 4608})

        test_json_input_stream = generate_skills_dict_input_stream(dirpath + '/no_synonyms_skills_dict.json')

        result = collector_adzuna(test_json_input_stream)

        assert m.call_count == 2
        assert result == json.dumps({"Java": 227, "Asana": 4608})


def test_error_raised_when_skills_dict_is_empty():

    test_json_input_stream = generate_skills_dict_input_stream(dirpath + '/empty_skills_dict.json')

    with pytest.raises(Exception) as error:
        collector_adzuna(test_json_input_stream)

    assert str(error.value) == 'inSkillsDict is empty, check skills_dict.json exists'


def test_create_keyword_query_returns_same_keyword_when_no_processing_needed():
    keyword = "Java"
    synonyms = test_dict[keyword]
    result = create_keyword_query(synonyms)
    expected = "what=java"

    assert result == expected


def test_create_keyword_query_returns_variants_of_skill_when_matches_key_in_skills_dict():
    keyword = "React"
    synonyms = test_dict[keyword]
    result = create_keyword_query(synonyms)
    expected = "what_or=react%20react.js%20reactjs"

    assert result == expected


def test_create_keyword_query_returns_a_what_phrase_when_multi_word_passed_in():
    keyword = 'Data Engineering'
    synonyms = test_dict[keyword]
    result = create_keyword_query(synonyms)
    expected = 'what_phrase=data%20engineering'

    assert result == expected


def test_create_keyword_query_returns_what_and_key_when_synonynms_contains_spaces():
    keyword = 'GCP'
    synonyms = test_dict[keyword]
    result = create_keyword_query(synonyms)
    expected = 'what=gcp'

    assert result == expected


def test_create_keyword_query_returns_encoded_chars():
    keyword = 'C#'
    synonyms = test_dict[keyword]
    result = create_keyword_query(synonyms)
    expected = 'what=c%23'

    assert result == expected


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_api_called_with_expected_url_when_phrases_present(mock):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what_phrase=data%20engineering&title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 4608})

        test_json_input_stream = generate_skills_dict_input_stream(dirpath + '/phrases_in_skills_dict.json')

        result = collector_adzuna(test_json_input_stream)

        assert m.call_count == 1
        assert result == json.dumps({"Data Engineering": 4608})


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_api_called_with_expected_url_when_single_word_synonyms_present(mock):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what_or=react%20react.js%20reactjs&title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 227})

        test_json_input_stream = generate_skills_dict_input_stream(dirpath + '/single_word_synonyms_in_skills_dict.json')

        result = collector_adzuna(test_json_input_stream)

        assert m.call_count == 1
        assert result == json.dumps({"React": 227})


@patch('collector_adzuna.app.get_secret_value', return_value='test')
def test_api_called_with_expected_url_when_multi_word_synonyms_present(mock):
    with requests_mock.Mocker() as m:
        m.get('http://api.adzuna.com/v1/api/jobs/gb/search/1?what=gcp&title_only=junior&location0=UK&category=it-jobs&content-type=application/json',
              json={"count": 100})

        test_json_input_stream = generate_skills_dict_input_stream(dirpath + '/multi_word_synonyms_in_skills_dict.json')

        result = collector_adzuna(test_json_input_stream)

        assert m.call_count == 1
        assert result == json.dumps({"GCP": 100})
