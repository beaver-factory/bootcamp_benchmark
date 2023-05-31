import json
import azure.functions as func
from collector_course_report import main

class OutBlobMock:
    def __init__(self):
        self.data = None

    def set(self, data):
        self.data = data

def test_main(mocker):
    # arrange
    mock_get_scraped_data = mocker.patch('collector_course_report.get_scraped_data')
    mock_get_scraped_data.return_value = {"foo": "bar"}

    mock_out_blob = OutBlobMock()

    # act
    main(None, mock_out_blob)

    # assert
    mock_get_scraped_data.assert_called_once()
    assert mock_out_blob.data == json.dumps({"foo": "bar"}).encode('utf-8')
