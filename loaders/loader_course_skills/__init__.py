from azure.functions import InputStream
from .app import load_course_skills_into_db


def main(inSkillsDict: InputStream):
    load_course_skills_into_db(inSkillsDict)
