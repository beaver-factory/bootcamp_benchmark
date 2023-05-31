from ..app import process_scraped_data
import pytest
import pandas as pd
import json


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
                    "course_desc": ""
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
                    "course_desc": ""
                }
            ],
            "meta": {
                "target_url": "",
                "timestamp": ""
            }
        }
    ]

    parsed_data = json.dumps(course_dict)


def test_raises_exception_on_incorrect_shape_at_first_level():
    test_dataframe = pd.DataFrame([{'test': 'string'}])
    with pytest.raises(Exception) as excinfo:
        process_scraped_data(test_dataframe)

    assert 'Missing required field' in str(excinfo.value)

def test_raises_exception_on_incorrect_shape_at_nest(expected_data_structure):
    error_structure = expected_data_structure
    del error_structure[0]['provider_courses'][0]['course_skills']
    df = pd.read_json(json.dumps(error_structure))

    with pytest.raises(Exception) as excinfo:
        process_scraped_data(df)

    assert 'Missing required field' in str(excinfo.value)


# def test_raises_exception_on_incorrect_type(expected_data_structure):

#     df = pd.read_json(expected_data_structure)

#     with pytest.raises(Exception) as excinfo:
#         process_scraped_data(df)

#     assert 'Field is wrong datatype' in str(excinfo.value)
