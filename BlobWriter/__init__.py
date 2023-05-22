import azure.functions as func
import logging
import json


def main(inBlob: func.InputStream, outBlob: func.Out[bytes]):
    logging.info(f'Function successfully triggered by blob: {inBlob.name}')
    jsonData= json.loads(inBlob.read())
    outBlob.set(jsonData)
    