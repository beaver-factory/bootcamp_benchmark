from unittest.mock import patch, Mock
from ..app import collector_adzuna
from dotenv import load_dotenv


load_dotenv()


def test_app():
    test_input_stream = generate_inputstream("./collector_adzuna/__tests__/test_skills.csv")

    result = collector_adzuna(test_input_stream)

    print(result)


def generate_inputstream(path):
    """converts a local csv file and returns a mocked blob input stream containing that data"""
    with open(path, 'r') as file:
        test_csv_data = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_csv_data

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream
