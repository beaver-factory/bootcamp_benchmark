import logging
import json
import azure.functions as func


def main(mytimer: func.TimerRequest, outBlob: func.Out[bytes]) -> None:
    logging.info('Timer Triggered a.json creation')

    a_json = {
        "name": 'test_func',
        "value": 'a'
    }

    mod_data = json.dumps(a_json)
    
    outBlob.set(mod_data.encode('utf-8'))
