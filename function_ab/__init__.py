import azure.functions as func
import json


def main(inBlob: func.InputStream, outBlob: func.Out[bytes]):
    # read json data from blob
    jsonData= json.loads(inBlob.read())

    # update value
    jsonData['value'] = 'ab'

    # jsonify it and set data in new blob
    # Note: this will completely overwrite the container. You would need to append data to the container then set it in reality.
    mod_data = json.dumps(jsonData)
    outBlob.set(mod_data.encode('utf-8'))
    