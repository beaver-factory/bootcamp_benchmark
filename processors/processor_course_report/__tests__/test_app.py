from ..app import process_course_data
from processor_utils import generate_inputstream
import pytest
from unittest.mock import patch
import pandas as pd
import json
import copy
import os


expected_data_structure = [
    {
        "provider_name": "test",
        "provider_locations": ["test"],
        "provider_tracks": ["test", "test", "test"],
        "provider_courses": [
            {
                "course_name": "test",
                "course_skills": ["test skill 1"],
                "course_locations": "York",
                "course_description": "test css"
            },
            {
                "course_name": "test",
                "course_skills": ["test skill 1", "test skill 2", "test skill 3"],
                "course_locations": "Manchester, York",
                "course_description": "test"
            }
        ],
        "meta": {
            "target_url": "test",
            "timestamp": "test"
        }
    },
    {
        "provider_name": "",
        "provider_locations": [""],
        "provider_tracks": [""],
        "provider_courses": [
            {
                "course_name": "",
                "course_skills": ["test skill 1"],
                "course_locations": "Birmingham, Online",
                "course_description": ""
            }
        ],
        "meta": {
            "target_url": "",
            "timestamp": ""
        }
    }

]

locations = {
    "uk_locations": ['York']
}

dirpath = 'processor_course_report/__tests__/skills_dict.json'


@pytest.fixture(scope="session", autouse=True)
def create_json():
    """Checks if test jsons are created, deletes if so, then generates fresh ones"""

    test_dict = {'Express': ['express', 'expressjs', 'express.js'], 'CSS': ['css', 'css3.0'], 'HTML': ['html', 'html5'], 'React': ['react', 'react.js', 'reactjs']}

    if os.path.isfile(dirpath):
        os.remove(dirpath)

    with open(f'{dirpath}', 'w') as file:
        file.write(json.dumps(test_dict))

    yield

    os.remove(dirpath)


@patch('azure.functions.Out')
def test_raises_exception_on_incorrect_shape_at_first_level(outBlob):
    inBlob = generate_inputstream(dirpath)
    test_dataframe = pd.DataFrame([{'test': 'string'}])
    with pytest.raises(KeyError) as excinfo:
        process_course_data(test_dataframe, locations["uk_locations"], inBlob, outBlob)

    assert 'provider_courses' in str(excinfo.value)


@patch('azure.functions.Out')
def test_raises_exception_on_incorrect_shape_at_nest(outBlob):
    inBlob = generate_inputstream(dirpath)
    error_structure = copy.deepcopy(expected_data_structure)
    del error_structure[0]['provider_courses'][0]['course_skills']
    del error_structure[0]['provider_courses'][1]['course_skills']
    del error_structure[1]['provider_courses'][0]['course_skills']
    df = pd.read_json(json.dumps(error_structure))

    with pytest.raises(KeyError) as excinfo:
        process_course_data(df, locations["uk_locations"], inBlob, outBlob)

    assert 'course_skills' in str(excinfo.value)


@patch('azure.functions.Out')
def test_returns_pandas_dataframe(outBlob):
    inBlob = generate_inputstream(dirpath)
    result = process_course_data(pd.read_json(
        json.dumps(expected_data_structure)), locations["uk_locations"], inBlob, outBlob)
    assert isinstance(result, pd.DataFrame)


@patch('azure.functions.Out')
def test_dataframe_contains_correct_columns(outBlob):
    inBlob = generate_inputstream(dirpath)
    result = process_course_data(pd.read_json(
        json.dumps(expected_data_structure)), locations["uk_locations"], inBlob, outBlob)
    expected = [
        'provider_name',
        'course_name',
        'course_skills',
        'course_locations',
        'target_url',
        'timestamp',
        'course_country'
    ]

    assert all(column in result.columns.values for column in expected)
    assert result.shape[1] == 7


@patch('azure.functions.Out')
def test_dataframe_contains_correct_number_of_rows(outBlob):
    inBlob = generate_inputstream(dirpath)
    result = process_course_data(pd.read_json(
        json.dumps(expected_data_structure)), locations["uk_locations"], inBlob, outBlob)
    assert result.shape[0] == 6


@patch('azure.functions.Out')
def test_dataframe_removes_rows_with_no_skills(outBlob):
    expected_data_structure.append(
        {
            "provider_name": "test2",
            "provider_locations": ["test2"],
            "provider_tracks": ["test2"],
            "provider_courses": [
                {
                    "course_name": "test2",
                    "course_skills": [],
                    "course_locations": "Birmingham, Online",
                    "course_description": "test2"
                }
            ],
            "meta": {
                "target_url": "",
                "timestamp": ""
            }
        })

    inBlob = generate_inputstream(dirpath)
    result = process_course_data(pd.read_json(
        json.dumps(expected_data_structure)), locations["uk_locations"], inBlob, outBlob)

    is_any_nulls = result['course_skills'].isnull().values.any()

    assert is_any_nulls is not True


@patch('azure.functions.Out')
def test_skills_column_gains_skills_from_description(outBlob):
    inBlob = generate_inputstream(dirpath)
    
    result = process_course_data(pd.read_json(
        json.dumps(expected_data_structure)), locations["uk_locations"], inBlob, outBlob)

    assert 'CSS' in result['course_skills'].values
