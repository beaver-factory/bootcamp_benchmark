from ..app import process_scraped_data
import pytest
import pandas as pd

@pytest.fixture(scope="session", autouse=True)
def expected_data_structure():
    return {
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

def test_raises_exception_on_incorrect_shape():
    test_dataframe = pd.DataFrame()
    with pytest.raises(Exception):
        process_scraped_data(test_dataframe)

def test_raises_exception_on_incorrect_type(expected_data_structure):

    df = pd.read_json(expected_data_structure)
    
    with pytest.raises(Exception) as excinfo:
        process_scraped_data(expected_data_structure)

    assert 'Field is wrong datatype' in str(excinfo.value)