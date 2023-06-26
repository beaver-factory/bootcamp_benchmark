import pandas as pd
import spacy
from spacy.matcher import Matcher


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
    
    existing_skills = [
        "CSS",
        "HTML",
        "JavaScript",
        "Ruby",
        "Express.js",
        "Front End",
        "Git",
        "Node.js",
        "Rails",
        "React.js",
        "SQL",
        "C#",
        "Design",
        "MongoDB",
        "User Experience Design",
        "Algorithms",
        "Data Structures",
        "PHP",
        "GitHub",
        "Agile",
        "iOS",
        "jQuery",
        "Swift",
        "Xcode",
        "AngularJS",
        "MySQL",
        "Quality Assurance Testing",
        "Scrum",
        "Java",
        "Cloud Computing",
        "Linux",
        "REST",
        "Django",
        "Python",
        "Data Engineering",
        "DevOps",
        "Data Visualization",
        "Data Science",
        "Data Analytics",
        "Artificial Intelligence",
        "MVC",
        "Product Management",
        "Machine Learning",
        "R",
        "Sinatra",
        "Mobile Security",
        "Business Intelligence",
        "Excel",
        "Growth Hacking",
        "Digital Marketing",
        "CompTIA Network+",
        "CompTIA Security+",
        "Cryptography",
        "Ethical Hacking",
        "Network Security",
        "Penetration Testing",
        "SIEM Administration",
        "Virtualization",
        "Mobile",
        "Wordpress",
        "Spark",
        "Networking",
        "ChatGPT",
        "Generative AI",
        "SEO",
        "Content Marketing",
        "Email Marketing",
        "Social Media Marketing",
        "NaN",
        "SEM",
        "Hadoop",
        ".NET",
        "Web3",
        "Solidity",
        "Blockchain",
        "Sales"
    ]

    supplemental_skills = [
        "Ruby on Rails",
        "Angular",
        "React",
        "Express",
        "Tableau",
        "PowerBI",
        "Heroku",
        "NodeJS",
        "Adobe Suite",
    ]

    base_skills = list(set(existing_skills + supplemental_skills))

    nlp = spacy.load("en_core_web_md")

    doc = nlp(description)

    matcher = Matcher(nlp.vocab)
    patterns = [[{"LOWER": word.lower()} for word in skill.split()] for skill in base_skills]
    matcher.add("SKILL", patterns, greedy="LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])

    skills = [doc[match[1]:match[2]].text for match in matches]

    return skills