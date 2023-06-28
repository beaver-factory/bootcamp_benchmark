import spacy
from negspacy.negation import Negex


def extract_skills(description, inSkillsDict):
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
    nlp.add_pipe("negex", after="ner", config={"ent_types":["SKILL"]})
    ruler = nlp.add_pipe("entity_ruler", before="ner")

    patterns = []
    full_patterns = []

    for skill in inSkillsDict:
        patterns.extend(inSkillsDict[skill])

    words_list = [word.split() for word in patterns]

    for words in words_list:
        pattern = [{"LOWER": word.lower()} for word in words]
        full_patterns.append(pattern)

    final_patterns = [{"label": "SKILL",  "pattern": pattern} for pattern in full_patterns]

    ruler.add_patterns(final_patterns)

    doc = nlp(description)

    result = []

    for ent in doc.ents:
        if ent.label_ == "SKILL" and ent._.negex == False:
            result.append(ent.text)

    return result