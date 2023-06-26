from processor_course_report.skill_deduper import check_edge_case_dict, handle_known_suffixes
from processor_utils import generate_inputstream
import pandas as pd
from unittest.mock import patch
import os
import pytest
import json

dirpath = 'processor_course_report/skill_deduper/__tests__/skills_dict.json'


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
def test_check_edge_case_dict_does_nothing_if_all_valid(outblob):
    new_inputstream = generate_inputstream(dirpath)
    skills = ['html', 'react', 'express']
    data = [{"course_skills": skill} for skill in skills]
    df = pd.DataFrame(data)

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"].tolist()

    assert skill_list[0] == 'HTML'
    assert outblob.set.call_count == 0


@patch('azure.functions.Out')
def test_check_edge_case_dict_replaces_values(outblob):
    new_inputstream = generate_inputstream(dirpath)
    skills = ['html5']
    data = [{"course_skills": skill} for skill in skills]
    df = pd.DataFrame(data)

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"].tolist()

    assert skill_list[0] == 'HTML'


@patch('azure.functions.Out')
def test_check_edge_case_dict_outputs_new_blob_only_if_difference(outblob):
    new_inputstream = generate_inputstream(dirpath)
    skills = ['test1', 'test2']
    data = [{"course_skills": skill} for skill in skills]
    df = pd.DataFrame(data)

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"].tolist()

    assert outblob.set.call_count == 1
    assert skill_list[0] == 'test1'

    skills = ['html']
    data = [{"course_skills": skill} for skill in skills]
    df = pd.DataFrame(data)

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"].tolist()

    assert outblob.set.call_count == 1
    assert skill_list[0] == 'HTML'


@patch('azure.functions.Out')
def test_check_edge_case_dict_outputs_same_case_df(outblob):
    new_inputstream = generate_inputstream(dirpath)
    skills = ['HTML']
    data = [{"course_skills": skill} for skill in skills]
    df = pd.DataFrame(data)

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"].tolist()

    assert skill_list[0] != 'html'


@patch('azure.functions.Out')
def test_check_edge_case_dict_outputs_full_df(outblob):
    new_inputstream = generate_inputstream(dirpath)
    skills = ['HTML', 'React']
    data = [{"provider_name": "Northcoders", "course_skills": skill} for skill in skills]
    df = pd.DataFrame(data)

    result = check_edge_case_dict(df, new_inputstream, outblob)
    prov_list = result["provider_name"].tolist()
    skill_list = result["course_skills"].tolist()

    assert prov_list[0] == 'Northcoders'
    assert len(prov_list) == 2
    assert skill_list[1] == 'React'
    assert len(skill_list) == 2


def test_handle_known_suffixes_removes_js():
    result_js = handle_known_suffixes('js')
    result_dot_js = handle_known_suffixes('node.js')
    result_nodejs = handle_known_suffixes('nodejs')

    assert result_js == 'js'
    assert result_dot_js == 'node'
    assert result_nodejs == 'node'


def test_handle_known_suffixes_removes_net():
    result_js = handle_known_suffixes('.net')
    result_dot_net = handle_known_suffixes('tech.net')
    result_technet = handle_known_suffixes('technet')

    assert result_js == '.net'
    assert result_dot_net == 'tech'
    assert result_technet == 'technet'


def generate_skills_dict():
    """Creates a json of skills for a test dictionary"""
