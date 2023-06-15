import json
from azure.functions import TimerRequest, Out
from .app import get_scraped_data


def main(mytimer: TimerRequest, outBlob: Out[bytes]) -> None:
    """Main Azure function for collector_course_report

    :param mytimer: Azure timer blob trigger
    :type mytimer: TimerRequest
    :param outBlob: Azure output blob
    :type outBlob: Out[bytes]
    """
    # create data whenever function is invoked
    scraped_data = get_scraped_data()
    # jsonify it and set data in new blob
    mod_data = json.dumps(scraped_data)
    outBlob.set(mod_data.encode('utf-8'))
