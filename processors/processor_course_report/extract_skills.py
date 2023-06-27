import spacy
from spacy.matcher import Matcher


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

    doc = nlp(description)

    filtered_tokens = []

    for token in doc:
        children = [child for child in token.head.children]
        if len(children) == 0:
            filtered_tokens.append(token.text)
        for i, child in enumerate(children):
            if child.dep_ == 'neg':
                break
            if i == len(children) - 1:
                filtered_tokens.append(token.text)

    filtered_doc = spacy.tokens.Doc(nlp.vocab, filtered_tokens)

    matcher = Matcher(nlp.vocab)

    skills_list = []

    for skill in inSkillsDict:
        skills_list.extend(inSkillsDict[skill])

    pattern_list = [
        [
            {"LOWER": word.lower()} for word in skill.split()
        ] for skill in skills_list
    ]

    matcher.add("SKILL", pattern_list, greedy="LONGEST")
    matches = matcher(filtered_doc)
    matches.sort(key = lambda x: x[1])

    skills = [filtered_doc[match[1]:match[2]].text for match in matches]

    return skills
