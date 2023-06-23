import spacy

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
        "Express"
    ]

    base_skills = existing_skills + supplemental_skills

    patterns = [
        {"label": "SKILL", "pattern": skill} for skill in base_skills
    ]

    nlp = spacy.load("en_core_web_md")
    ruler = nlp.add_pipe("entity_ruler", before='ner')
    ruler.add_patterns(patterns)

    doc = nlp(description)

    skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']

    print(skills)

    return skills
