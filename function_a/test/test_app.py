import pytest
from function_a.app import app

def test_app():
    output = app()

    assert output['name'] == 'test_func'
    assert output['value'] == 'a'
