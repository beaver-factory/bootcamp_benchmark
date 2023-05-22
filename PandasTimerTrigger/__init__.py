import logging
import pandas as pd

import azure.functions as func


def main(pandastimertrigger: func.TimerRequest) -> None:
    dataframe = pd.DataFrame({'Yes': [50,21], 'No': [131,2]})

    dataframe_length = len(dataframe)

    logging.info(f'{dataframe_length} - this is a pandas function test')
