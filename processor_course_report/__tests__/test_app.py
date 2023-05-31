from ..app import process_scraped_data
import pytest
import pandas as pd
import json


@pytest.fixture(scope="session", autouse=True)
def expected_data_structure():
    course_dict = [{
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

    return parsed_data


def test_raises_exception_on_incorrect_shape():
    test_dataframe = pd.DataFrame()
    with pytest.raises(Exception) as excinfo:
        process_scraped_data(test_dataframe)

    # assert 'Missing required field' in str(excinfo.value)
    assert False


def test_raises_exception_on_incorrect_type(expected_data_structure):

    df = pd.read_json(expected_data_structure)

    with pytest.raises(Exception) as excinfo:
        process_scraped_data(df)

    assert 'Field is wrong datatype' in str(excinfo.value)
