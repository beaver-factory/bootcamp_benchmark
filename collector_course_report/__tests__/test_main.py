import pytest
import json
import azure.functions as func
from collector_course_report import main

def test_main(mocker):
    # arrange
    mock_get_scraped_data = mocker.patch('collector_course_report.get_scraped_data')
    mock_get_scraped_data.return_value = {"foo": "bar"}

    mock_out_blob = mocker.Mock(spec=func.Out[bytes])

    # act
    main(None, mock_out_blob)

    # assert
    mock_get_scraped_data.assert_called_once()
    mock_out_blob.set.assert_called_once_with(json.dumps({"foo": "bar"}).encode('utf-8'))
