import azure.functions as func
# import pandas as pd
from .app import load_course_report_into_db


def main(inBlob: func.InputStream):
    # read data from blob and store as data frame
    # input_df = pd.read_csv(inBlob.read())

    # load data frame into db
    load_course_report_into_db(inBlob)
