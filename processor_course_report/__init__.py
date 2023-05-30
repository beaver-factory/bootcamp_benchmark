import azure.functions as func
import pandas as pd
from .app import app
from io import BytesIO


def main(inBlob: func.InputStream, outBlob: func.Out[bytes]):

    input_df = pd.read_json(BytesIO(inBlob.read()))

    output_df = app(input_df)

    output = output_df.to_csv()

    outBlob.set(output.encode('utf-8'))
