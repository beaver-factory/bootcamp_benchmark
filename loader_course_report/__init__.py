import azure.functions as func
from .app import load_course_report_into_db, load_course_skills_into_db


def main(inBlob: func.InputStream, blobName: str):
    if 'processed_course_data_' in blobName:
        load_course_report_into_db(inBlob)

    if 'processed_skills_data_' in blobName:
        load_course_skills_into_db(inBlob)
