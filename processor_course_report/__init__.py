import azure.functions as func
import pandas as pd
from .app import app


def main(inBlob: func.InputStream, outBlob: func.Out[str]):

    input_df = pd.read_json(inBlob.read())

    output_df = app(input_df)

    output = output_df.to_csv()

    outBlob.set(output.encode('utf-8'))
