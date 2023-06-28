from ..extract_skills import extract_skills
from processor_utils import generate_inputstream
import os
import json
import pytest

test_input = "As a Software Engineer graduate you will be ready to start a career in a variety of coding roles. Throughout this bootcamp you will learn to: create front-end web application with modern JavaScript frameworks such as Angular or React, develop full-stack applications with in-demand technologies such as Ruby on Rails, Python with Django, and Express with Node.js, and integrate third-party application programming interfaces (APIs) in an application."

test_input2 = "Become a software engineer in 13 weeks at our coding bootcamps in Manchester, Leeds, Newcastle, Birmingham and remotely. Unlike our Data Engineering bootcamp where you focus specifically on the 'back-end' of software, or our DevOps Engineering bootcamp that deals specifically with software development and IT operations, our coding bootcamp focuses on building websites and mobile phone apps. The application process takes 2-3 weeks and we would advise you to apply sooner rather than later to give yourself plenty of time to work through the preparation materials. Applicants living in England can apply for DfE funding to cover the entire cost of the course. Get in touch to find out if you qualify."

test_input3 = "As a Data Analyst graduate you will be able to problem solve and effectively communicate like an analyst. This course teaches you to use industry-standard tools to make ethical, data-driven decisions. Experience hands-on training to master SQL, Excel, Tableau, PowerBI, and Python – tools listed in virtually every data analytics job posting across industries."

test_input4 = "The course is designed for everyone, whether a complete novice, a computer science graduate wanting practical experience, or an entrepreneur sick of looking for a technical co-founder. Students learn an incredible amount, including: Ruby on Rails; HTML5 and CSS3; time management; communication skills; customer service; Agile and Lean Development; JavaScript, jQuery and NodeJS; along with Git and Heroku, and software design best practices. Students learn through first hand experience, community-driven classrooms, pairing, and project-based work."

test_input5 = "On our Data Science course, you will learn the fundamentals of this discipline, including Python, how to make dashboards using PowerBI, database management and PSQL. We do not cover JavaScript, Front End nor how to make a website using HTML."

dirpath = "processor_course_report/__tests__/skills_dict.json"


@pytest.fixture(scope="session", autouse=True)
def create_json():
    """Checks if test jsons are created, deletes if so, then generates fresh ones"""

    test_dict = {"JavaScript": ["Javascript"], "Angular": ["Angular"], "Ruby on Rails": ["Ruby on Rails"], "React": ["react", "react.js", "reactjs"], "Python": ["Python"], "Django": ["Django"], "Express": ["Express"], "Node.js": ["Node.js"], "SQL": ["SQL"], "Excel": ["Excel"], "PowerBI": ["PowerBI"], "Tableau": ["Tableau"], "CSS": ["CSS"], "HTML": ["HTML"], "Bootstrap": ["Bootstrap"]}

    if os.path.isfile(dirpath):
        os.remove(dirpath)

    with open(f"{dirpath}", "w") as file:
        file.write(json.dumps(test_dict))

    yield

    os.remove(dirpath)


def test_returns_correct_typing():
    new_inputstream = generate_inputstream(dirpath)

    skills_stream = new_inputstream.read().decode("utf-8")

    skills_dict = json.loads(skills_stream)

    result = extract_skills(test_input, skills_dict)

    for skill in result:
        assert type(skill) is str


def test_returns_expected_list_of_skills():
    new_inputstream = generate_inputstream(dirpath)

    skills_stream = new_inputstream.read().decode("utf-8")

    skills_dict = json.loads(skills_stream)

    result = extract_skills(test_input, skills_dict)

    expected = ["JavaScript", "Angular", "React", "Ruby on Rails", "Python", "Django", "Express", "Node.js"]

    assert sorted(result) == sorted(expected)


def test_returns_correct_skills():
    new_inputstream = generate_inputstream(dirpath)

    skills_stream = new_inputstream.read().decode("utf-8")

    skills_dict = json.loads(skills_stream)

    result = extract_skills(test_input3, skills_dict)
    expected = ["SQL", "Excel", "PowerBI", "Tableau", "Python"]

    assert sorted(result) == sorted(expected)


def test_raises_exception_on_incorrect_input_type():
    new_inputstream = generate_inputstream(dirpath)

    skills_stream = new_inputstream.read().decode("utf-8")

    skills_dict = json.loads(skills_stream)

    with pytest.raises(Exception) as e:
        extract_skills(123, skills_dict)

    assert str(e.value) == "Input must be str"


def test_ignores_skills_when_negative():
    new_inputstream = generate_inputstream(dirpath)

    skills_stream = new_inputstream.read().decode("utf-8")

    skills_dict = json.loads(skills_stream)

    test_str = 'Not JavaScript'
    test_str2 = 'Definitely not JavaScript'
    test_str3 = 'We don\'t teach JavaScript on this course.'

    result = extract_skills(test_str, skills_dict)
    result2 = extract_skills(test_str2, skills_dict)
    result3 = extract_skills(test_str3, skills_dict)

    assert len(result) == 0
    assert len(result2) == 0
    assert len(result3) == 0


def test_ignores_unlike():
    new_inputstream = generate_inputstream(dirpath)

    skills_stream = new_inputstream.read().decode("utf-8")

    skills_dict = json.loads(skills_stream)

    result = extract_skills(test_input2, skills_dict)

    expected = []

    assert result == expected


def test_extracts_from_full_description():
    test_input = 'Students will create two websites (a 1-page website and a 5-page website) over the course of 12 weeks. Students will learn to code in HTML, CSS and Javascript. Students will experience the following: \r\n\r\n-Discover FTP (File Transfer Process) website servers\r\n-Develop link building skills\r\n-Learn the Bootstrap framework for responsive design\r\n-Learn how to font with Awesome icons\r\n-Learn how to use Photoshop\r\n-Learn how to implement contact forms.'

    new_inputstream = generate_inputstream(dirpath)

    skills_stream = new_inputstream.read().decode("utf-8")

    skills_dict = json.loads(skills_stream)

    result = extract_skills(test_input, skills_dict)

    expected = ['HTML', 'CSS', 'Javascript', 'Bootstrap']

    assert sorted(result) == sorted(expected)


def test_ignores_negated_skills_in_full_description():
    test_input = 'Students will create two websites (a 1-page website and a 5-page website) over the course of 12 weeks. Students will learn to code in HTML, CSS and Javascript. Students will experience the following: \r\n\r\n-Discover FTP (File Transfer Process) website servers\r\n-Develop link building skills\r\n-Learn the Bootstrap framework for responsive design\r\n-Learn how to font with Awesome icons\r\n-Learn how to use Photoshop\r\n-Learn how to implement contact forms. We do not teach Python, React, or Ruby on Rails'

    new_inputstream = generate_inputstream(dirpath)

    skills_stream = new_inputstream.read().decode("utf-8")

    skills_dict = json.loads(skills_stream)

    result = extract_skills(test_input, skills_dict)

    expected = ['HTML', 'CSS', 'Javascript', 'Bootstrap']

    assert sorted(result) == sorted(expected)
