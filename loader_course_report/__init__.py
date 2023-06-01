import azure.functions as func
from .app import load_course_report_into_db


def main(inBlob: func.InputStream):
    load_course_report_into_db(inBlob)
