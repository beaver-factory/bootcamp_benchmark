import azure.functions as func
from .app import load_course_report_into_db, load_course_skills_into_db


def main(inBlob: func.InputStream):
    if 'course_report_courses' in inBlob.name:
        load_course_report_into_db(inBlob)

    if 'course_report_skills' in inBlob.name:
        load_course_skills_into_db(inBlob)
