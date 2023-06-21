from processor_course_report.skill_deduper import skill_deduper
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def test_outputs_df():
    test_empty_dataframe = pd.DataFrame([{"skills": ['html', 'html5', 'css', 'css3', 'css7']}])

    result = skill_deduper(test_empty_dataframe)

    result_arr = result['skills'][0]

    assert result_arr == ['html', 'html5', 'css', 'css3']


def test_removes_similar_values():
    test_react_dataframe = pd.DataFrame([{"skills": ['react', 'React', 'react.js', 'React.js', 'react.JS', 'React.JS']}])

    result = skill_deduper(test_react_dataframe)

    result_arr = result['skills'][0]

    assert result_arr == ['react']
