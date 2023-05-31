import unittest
from unittest.mock import MagicMock, patch
import importlib
import azure.functions as func
import collector_course_report


class TestMain(unittest.TestCase):

    @patch('collector_course_report.app.get_scraped_data', return_value={'foo': 'bar'})
    def test_main(self, mock_get_scraped_data):
        # annoyingly have to reload module to ensure that the foobar mock is applied
        importlib.reload(collector_course_report)

        # arrange
        mytimer = MagicMock()
        outBlob = MagicMock(spec=func.Out[bytes], autospec=True)

        # act
        collector_course_report.main(mytimer, outBlob)

        # assert
        mock_get_scraped_data.assert_called_once()
        outBlob.set.assert_called_once_with(b'{"foo": "bar"}')


if __name__ == '__main__':
    unittest.main()
