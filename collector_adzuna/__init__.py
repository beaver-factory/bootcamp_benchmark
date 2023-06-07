from .app import collector_adzuna
import azure.functions as func
import json


def main(mytimer: func.TimerRequest, outBlob: func.Out[bytes]) -> None:

    api_data = collector_adzuna()

    json_data = json.dumps(api_data)
    outBlob.set(json_data.encode('utf-8'))
