import spacy
from negspacy.negation import Negex  # noqa:F401
from typing import List, Dict


def extract_skills(description: str, inSkillsDict: Dict) -> List[str]:
    """Runs description through spaCy NLP model to return a list of digital skills from a given course description


    Args:
        description (str): Course description from which to extract skills
        inSkillsDict (Dict): Dictionary of skill root words each with a List of synonyms as values.

    Raises:
        Exception: Checks that description passed in is of type str

    Returns:
        List[str]: List of skills that have been extracted
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
        pattern = generate_pattern(words)
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

def generate_pattern(words: List[str]) -> List[Dict]:
    """Generates spacy entity pattern

    :param words: List of individual skills
    :type words: List[str]
    :return: Spacy entity ruler patterns
    :rtype: List[Dict]
    """
    pattern = []

    for word in words:
        if '-' in word: 
            tokens = word.split('-')
            token_patterns = [{'LOWER': token.lower()} for token in tokens]
            token_patterns.insert(1,{'IS_PUNCT': True})
            pattern.extend(token_patterns)
            continue

        pattern.append({"LOWER": word.lower()})

    return pattern