from thefuzz import fuzz
from thefuzz import process
import json

with open('./dummy_skills.json') as file:
    results = json.load(file)

result = results['result'][0]

global_skills = ["CSS", "HTML", "JavaScript", "Ruby", "Express.js", "Front End", "Git", "Node.js", "Rails", "React.js", "SQL", "C#", "Typescript", ".Net", "PSQL", "MySQL", "NoSQL"]


def remove_duplicate_skills(input):

    skills_present = []

    for skill in input:
        similarities = process.extract(skill, global_skills)
        print(skill, similarities)
        for similarity in similarities:
            if similarity[1] >= 90:
                skills_present.append(similarity[0])

    unique_skills = list(dict.fromkeys((skills_present)))
    print(unique_skills)
    return unique_skills


for result in results['result']:
    remove_duplicate_skills(result)
