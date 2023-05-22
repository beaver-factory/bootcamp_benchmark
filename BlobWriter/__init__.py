import azure.functions as func
import logging
import json


def main(inBlob: func.InputStream, outBlob):
    logging.info(inBlob['name'])
    