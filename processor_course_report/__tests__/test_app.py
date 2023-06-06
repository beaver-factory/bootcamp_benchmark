from ..app import (process_scraped_data)
import pytest
import pandas as pd
import json
import copy


expected_data_structure = [
    {
        "provider_name": "test",
        "provider_locations": ["test"],
        "provider_tracks": ["test", "test", "test"],
        "provider_courses": [
            {
                "course_name": "test",
                "course_skills": ["test"],
                "course_locations": "test",
                "course_description": "test"
            },
            {
                "course_name": "test",
                "course_skills": ["test1", "test2", "test3"],
                "course_locations": "Manchester",
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


def test_raises_exception_on_incorrect_shape_at_nest():
    error_structure = copy.deepcopy(expected_data_structure)
    del error_structure[0]['provider_courses'][0]['course_skills']
    del error_structure[0]['provider_courses'][1]['course_skills']
    del error_structure[1]['provider_courses'][0]['course_skills']
    df = pd.read_json(json.dumps(error_structure))

    with pytest.raises(KeyError) as excinfo:
        process_scraped_data(df)

    assert 'course_skills' in str(excinfo.value)


def test_returns_pandas_dataframe():
    result = process_scraped_data(pd.read_json(
        json.dumps(expected_data_structure)))
    assert isinstance(result, pd.DataFrame)


def test_dataframe_contains_correct_columns():
    result = process_scraped_data(pd.read_json(
        json.dumps(expected_data_structure)))
    expected = [
        'provider_name',
        'course_name',
        'course_skills',
        'course_locations',
        'course_description',
        'target_url',
        'timestamp',
        'course_country'
    ]

    assert all(column in result.columns.values for column in expected)
    assert result.shape[1] == 8


def test_dataframe_contains_correct_number_of_rows():
    result = process_scraped_data(pd.read_json(
        json.dumps(expected_data_structure)))

    assert result.shape[0] == 3
