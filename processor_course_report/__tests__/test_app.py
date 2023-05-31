from ..app import process_scraped_data
import pytest
import pandas as pd
import json
import copy


@pytest.fixture(scope="session", autouse=False)
def expected_data_structure():
    return [
        {
            "provider_name": "",
            "provider_locations": [""],
            "provider_tracks": [""],
            "provider_courses": [
                {
                    "course_name": "",
                    "course_skills": [""],
                    "course_locations": "",
                    "course_description": ""
                }
            ],
            "meta": {
                "target_url": "",
                "timestamp": ""
            }
        },
        {
            "provider_name": "",
            "provider_locations": [""],
            "provider_tracks": [""],
            "provider_courses": [
                {
                    "course_name": "",
                    "course_skills": [""],
                    "course_locations": "",
                    "course_description": ""
                }
            ],
            "meta": {
                "target_url": "",
                "timestamp": ""
            }
        }
    ]


def test_raises_exception_on_incorrect_shape_at_first_level():
    test_dataframe = pd.DataFrame([{'test': 'string'}])
    with pytest.raises(KeyError) as excinfo:
        process_scraped_data(test_dataframe)

    assert 'provider_courses' in str(excinfo.value)


def test_raises_exception_on_incorrect_shape_at_nest(expected_data_structure):
    error_structure = copy.deepcopy(expected_data_structure)
    del error_structure[0]['provider_courses'][0]['course_skills']
    del error_structure[1]['provider_courses'][0]['course_skills']
    df = pd.read_json(json.dumps(error_structure))

    with pytest.raises(KeyError) as excinfo:
        process_scraped_data(df)

    assert 'course_skills' in str(excinfo.value)

def test_returns_pandas_dataframe(expected_data_structure):
    result = process_scraped_data(pd.read_json(json.dumps(expected_data_structure)))
    assert isinstance(result, pd.DataFrame)

def test_dataframe_contains_correct_columns(expected_data_structure):
    result = process_scraped_data(pd.read_json(json.dumps(expected_data_structure)))
    expected = [
        'provider_name',
        'provider_tracks',
        'course_name',
        'course_skills',
        'course_locations',
        'course_description',
        'time',
        'target_url',
        'timestamp'
    ]

    assert all(column in result.columns.values for column in expected)

def test_dataframe_contains_correct_number_of_rows(expected_data_structure):
    result = process_scraped_data(pd.read_json(json.dumps(expected_data_structure)))
    assert result.shape[0] == 2
