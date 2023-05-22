import azure.functions as func
import logging
import json


def main(inBlob: func.InputStream, outBlob: func.Out[bytes]):
    logging.info(f'Function successfully triggered by blob: {inBlob.name}')

    jsonData= json.loads(inBlob.read())

    jsonData['value'] = 'ab'

    logging.info(jsonData['value'])

    mod_data = json.dumps(jsonData)
    
    outBlob.set(mod_data.encode('utf-8'))
    