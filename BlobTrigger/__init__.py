import azure.functions as func
import logging

def main(myBlob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myBlob.name}\n"
                 f"blob Size: {myBlob.length} bytes")
    
    