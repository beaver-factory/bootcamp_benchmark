import spacy
from spacy.matcher import Matcher
import json

def extract_skills(description):
    """
    Runs an openAI API query to return a list of digital skills from a given course description

    :param description: a string detailing what a bootcamp course offers
    :type description: string
    :return: list of digital skills included in the course description
    :rtype: list
    """

    if type(description) != str:
        raise Exception("Input must be str")

    nlp = spacy.load("en_core_web_md")

    doc = nlp(description)

    matcher = Matcher(nlp.vocab)
    with open('./processor_course_report/skill_deduper/skills_dict.json', 'r') as f:
        skill_dict = json.load(f)

    skills_list = []

    for skill in skill_dict:
        skills_list.extend(skill_dict[skill])

    pattern_list = [
        [
            {"LOWER": word.lower()} for word in skill.split()
        ] for skill in skills_list
    ]
    
    matcher.add("SKILL", pattern_list, greedy="LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])

    skills = [doc[match[1]:match[2]].text for match in matches]

    return skills