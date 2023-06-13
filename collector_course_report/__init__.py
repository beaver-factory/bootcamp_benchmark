import json
import azure.functions as func
from .app import get_scraped_data


def main(mytimer: func.TimerRequest, outBlob: func.Out[bytes]) -> None:
    # create data whenever function is invoked
    scraped_data = get_scraped_data()
    # jsonify it and set data in new blob
    mod_data = json.dumps(scraped_data)
    outBlob.set(mod_data.encode('utf-8'))
