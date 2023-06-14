from ..app import get_scraped_data
import json
import pytest


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


@pytest.fixture(scope="session", autouse=True)
def actual_data():
    actual_data = get_scraped_data()
    actual_parsed_data = json.loads(json.dumps(actual_data))
    return actual_parsed_data


@pytest.mark.skip(reason='run once takes forever')
def test_generate_example_report(actual_data):
    results = actual_data

    save_file = open(
        './collector_course_report/__tests__/test_output_course_report_data.json', 'w')

    json.dump(results, save_file, indent=6)

    save_file.close()


def test_spider_returns_expected_data_structure(expected_data_structure, actual_data):
    expected_keys = expected_data_structure.keys()

    actual_parsed_keys = actual_data[1].keys()

    assert expected_keys == actual_parsed_keys


def test_spider_returns_data(actual_data, expected_data_structure):
    expected_keys = expected_data_structure.keys()

    for key in expected_keys:
        assert actual_data[1][key] is not None
