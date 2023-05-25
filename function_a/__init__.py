import json
import azure.functions as func
from .app import app


def main(mytimer: func.TimerRequest, outBlob: func.Out[bytes]) -> None:
    # create data whenever function is invoked
    a_json = app()
    # jsonify it and set data in new blob
    # Note: this will completely overwrite the container.
    # You would need to append data to the container then set it in reality.
    mod_data = json.dumps(a_json)
    outBlob.set(mod_data.encode('utf-8'))
