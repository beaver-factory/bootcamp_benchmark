import spacy
from negspacy.negation import Negex  # noqa:F401
from typing import List, Dict


def extract_skills(description: str, inSkillsDict: Dict) -> List[str]:
    """Extracts skills from description string

    :param description: course description
    :type description: str
    :param inSkillsDict: dictionary of skills
    :type inSkillsDict: Dict
    :raises Exception: checks if description is not string
    :return: list of skills
    :rtype: List[str]
    """

    if type(description) != str:
        raise Exception("Input must be str")

    nlp = spacy.load("en_core_web_md")
    nlp.add_pipe("negex", after="ner", config={"ent_types": ["SKILL"]})
    ruler = nlp.add_pipe("entity_ruler", before="ner")

    patterns = []
    full_patterns = []

    for skill in inSkillsDict:
        patterns.extend(inSkillsDict[skill])

    words_list = [word.split() for word in patterns]

    for words in words_list:
        pattern = [{"LOWER": word.lower()} for word in words]
        full_patterns.append(pattern)

    final_patterns = [{"label": "SKILL", "pattern": pattern} for pattern in full_patterns]

    ruler.add_patterns(final_patterns)

    doc = nlp(description)

    words_to_remove = ["Unlike", "unlike"]

    filtered_sents = []

    for sent in doc.sents:
        if not any(word in sent.text for word in words_to_remove):
            filtered_sents.append(sent.text)

    filtered_doc = nlp(" ".join(filtered_sents))

    result = []

    for ent in filtered_doc.ents:
        if ent.label_ == "SKILL" and ent._.negex is False:
            result.append(ent.text)

    return result
