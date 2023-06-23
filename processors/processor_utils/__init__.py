from unittest.mock import patch, Mock


def generate_inputstream(path: str):
    """Converts a local csv file to a mock azure inputstream format

    :param path: path of a local csv file
    :type path: str
    :return: a mocked azure blob input stream containing the csv data
    :rtype: InputStream
    """

    with open(path, 'rb') as file:
        test_json_data = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_json_data

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream
