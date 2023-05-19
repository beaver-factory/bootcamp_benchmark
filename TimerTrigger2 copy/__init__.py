import datetime
import logging
import pandas as pd

import azure.functions as func


def main(pandastimertrigger: func.TimerRequest) -> None:
    dataframe = pd.DataFrame({'Yes': [50,21], 'No': [131,2]})
    
    logging.info(f'{len(dataframe)} - heres a pandas test! this value should be 2')
    
