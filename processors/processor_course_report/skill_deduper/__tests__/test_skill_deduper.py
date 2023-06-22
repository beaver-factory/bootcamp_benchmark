from processor_course_report.skill_deduper import skill_deduper, prep_prompt_input, check_edge_case_dict
import pandas as pd
from dotenv import load_dotenv
import pytest
from unittest.mock import patch

load_dotenv()


@patch("openai.Completion.create", return_value={"choices": [{"text": "html"}]})
def test_outputs_df(openai_mock):
    test_empty_dataframe = pd.DataFrame([{"skills": ["html"]}])

    result = skill_deduper(test_empty_dataframe)

    assert openai_mock.call_count == 1
    assert isinstance(result, pd.DataFrame)
    assert result["skills"][0] == ["html"]


@pytest.mark.skip(reason='avoid OpenAI API call')
def test_removes_similar_values():
    test_react_dataframe = pd.DataFrame([{"skills": ['react', 'React', 'react.js', 'React.js', 'react.JS', 'React.JS']}])

    result = skill_deduper(test_react_dataframe)

    result_arr = result['skills'][0]

    assert result_arr == ['react']


def test_prep_prompt_input_sorts_alphabetically():
    skills = ["react", "html", "css"]
    df = pd.DataFrame([{"skills": skills}])

    result = prep_prompt_input(df)

    expected = ["css", "html", "react"]
    assert result == expected


def test_prep_prompt_input_lowercases_everything():
    skills = ["Javascript", "postgreSQL", "react.JS"]
    df = pd.DataFrame([{"skills": skills}])

    result = prep_prompt_input(df)

    expected = ["javascript", "postgresql", "react.js"]
    assert result == expected


def test_prep_prompt_input_returns_only_unique_values():
    skills = ["react", "react.JS", "react.js"]
    df = pd.DataFrame([{"skills": skills}])

    result = prep_prompt_input(df)

    expected = ["react", "react.js"]
    assert result == expected


def test_prep_prompt_input_raises_exception_when_passed_empty_skills_list():
    skills = []
    df = pd.DataFrame([{"skills": skills}])

    with pytest.raises(Exception) as error:
        prep_prompt_input(df)

    assert str(error.value) == "Cannot prep prompt, list of skills is empty"


def test_check_edge_case_dict_removes_edge_case():
    skills = ["react", "html", "html5"]

    result = check_edge_case_dict(skills)

    expected = ["react", "html"]
    assert result == expected


def test_check_edge_case_dict_returns_empty_string_when_passed_empty_string():
    skills = [""]

    result = check_edge_case_dict(skills)

    expected = [""]
    assert result == expected


def test_check_edge_case_dict_updates_single_edge_case_skill():
    skills = ["react", "html5"]

    result = check_edge_case_dict(skills)

    expected = ["react", "html"]
    assert result == expected
