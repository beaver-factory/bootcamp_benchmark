from processor_course_report.skill_deduper import check_edge_case_dict
from processor_utils import generate_inputstream
import pandas as pd
from dotenv import load_dotenv
import pytest
from unittest.mock import patch
from io import BytesIO

load_dotenv()

dirpath = 'processor_course_report/skill_deduper/skills_dict.json'


@patch('azure.functions.Out')
def test_check_edge_case_dict_does_nothing_if_all_valid(outblob):
    new_inputstream = generate_inputstream(dirpath)
    df = pd.DataFrame([{"course_skills": ['html', 'react', 'express']}])

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"][0]

    assert skill_list[0] == 'html'
    assert outblob.set.call_count == 0


@patch('azure.functions.Out')
def test_check_edge_case_dict_replaces_values(outblob):
    new_inputstream = generate_inputstream(dirpath)
    df = pd.DataFrame([{"course_skills": ['html5']}])

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"][0]

    assert skill_list[0] == 'html'


@patch('azure.functions.Out')
def test_check_edge_case_dict_outputs_new_blob_only_if_difference(outblob):
    new_inputstream = generate_inputstream(dirpath)
    df = pd.DataFrame([{"course_skills": ['test1', 'test2']}])

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"][0]

    assert outblob.set.call_count == 1
    assert skill_list[0] == 'test1'

    df = pd.DataFrame([{"course_skills": ['html']}])

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"][0]

    assert outblob.set.call_count == 1
    assert skill_list[0] == 'html'


@patch('azure.functions.Out')
def test_check_edge_case_dict_outputs_lowercase_df(outblob):
    new_inputstream = generate_inputstream(dirpath)
    df = pd.DataFrame([{"course_skills": ['HTML']}])

    result = check_edge_case_dict(df, new_inputstream, outblob)
    skill_list = result["course_skills"][0]

    assert skill_list[0] == 'html'
