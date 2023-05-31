import azure.functions as func
import pandas as pd
from .app import process_scraped_data


def main(inBlob: func.InputStream, outBlob: func.Out[bytes]):

    input_df = pd.read_json(inBlob.read())

    output_df = process_scraped_data(input_df)

    output = output_df.to_csv()

    outBlob.set(output.encode('utf-8'))
