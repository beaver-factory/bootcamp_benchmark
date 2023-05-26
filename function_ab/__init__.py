import azure.functions as func
import pandas as pd
from .app import app


def main(inBlob: func.InputStream, outBlob: func.Out[bytes]):
    # consider refactoring conversion from dataframe to
    # json and then df to csv into another function
    print(inBlob.read())
    # read json data from blob
    input_df = pd.read_json(inBlob.read())

    output_df = app(input_df)

    output = output_df.to_csv()

    outBlob.set(output.encode('utf-8'))
