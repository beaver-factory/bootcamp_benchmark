from ..extract_skills import extract_skills
import pytest

test_input = "As a Software Engineer graduate you will be ready to start a career in a variety of coding roles. Throughout this bootcamp you will learn to: create front-end web application with modern JavaScript frameworks such as Angular or React, develop full-stack applications with in-demand technologies such as Ruby on Rails, Python with Django, and Express with Node.js, and integrate third-party application programming interfaces (APIs) in an application."

test_input2 = "Become a software engineer in 13 weeks at our coding bootcamps in Manchester, Leeds, Newcastle, Birmingham and remotely. Unlike our Data Engineering bootcamp where you focus specifically on the 'back-end' of software, or our DevOps Engineering bootcamp that deals specifically with software development and IT operations, our coding bootcamp focuses on building websites and mobile phone apps. The application process takes 2-3 weeks and we would advise you to apply sooner rather than later to give yourself plenty of time to work through the preparation materials. Applicants living in England can apply for DfE funding to cover the entire cost of the course. Get in touch to find out if you qualify."

test_input3 = "As a Data Analyst graduate you will be able to problem solve and effectively communicate like an analyst. This course teaches you to use industry-standard tools to make ethical, data-driven decisions. Experience hands-on training to master SQL, Excel, Tableau, PowerBI, and Python – tools listed in virtually every data analytics job posting across industries."

test_input4 = "The course is designed for everyone, whether a complete novice, a computer science graduate wanting practical experience, or an entrepreneur sick of looking for a technical co-founder. Students learn an incredible amount, including: Ruby on Rails; HTML5 and CSS3; time management; communication skills; customer service; Agile and Lean Development; JavaScript, jQuery and NodeJS; along with Git and Heroku, and software design best practices. Students learn through first hand experience, community-driven classrooms, pairing, and project-based work."

test_input5 = "On our Data Science course, you will learn the fundamentals of this discipline, including Python, how to make dashboards using Power BI, database management and PSQL. We do not cover JavaScript, Front End nor how to make a website using HTML."

dirpath = "processor_course_report/__tests__/extraction_skills_dict.json"

test_dict = {"JavaScript": ["javascript"], "Angular": ["angular"], "Ruby on Rails": ["ruby on rails"], "React": ["react", "react.js", "reactjs"], "Python": ["python"], "Django": ["django"], "Express": ["express"], "Node.js": ["node.js"], "SQL": ["sql"], "Excel": ["excel"], "Power BI": ["power bi", "powerbi"], "Tableau": ["tableau"], "CSS": ["css"], "HTML": ["html"], "Bootstrap": ["bootstrap"], "Agile": ["agile methodology", "agile principles", "agile"], "Object-oriented programming": ["object-oriented programming"]}


def test_returns_correct_typing():

    result = extract_skills(test_input, test_dict)

    for skill in result:
        assert type(skill) is str


def test_returns_expected_list_of_skills():

    result = extract_skills(test_input, test_dict)

    expected = ["JavaScript", "Angular", "React", "Ruby on Rails", "Python", "Django", "Express", "Node.js"]

    assert sorted(result) == sorted(expected)


def test_returns_correct_skills():

    result = extract_skills(test_input3, test_dict)

    expected = ["SQL", "Excel", "PowerBI", "Tableau", "Python"]

    assert sorted(result) == sorted(expected)


def test_raises_exception_on_incorrect_input_type():

    with pytest.raises(Exception) as e:
        extract_skills(123, test_dict)

    assert str(e.value) == "Input must be str"


def test_ignores_skills_when_negative():

    test_str = 'Not JavaScript'
    test_str2 = 'Definitely not JavaScript'
    test_str3 = 'We don\'t teach JavaScript on this course.'

    result = extract_skills(test_str, test_dict)
    result2 = extract_skills(test_str2, test_dict)
    result3 = extract_skills(test_str3, test_dict)

    assert len(result) == 0
    assert len(result2) == 0
    assert len(result3) == 0


def test_ignores_unlike():

    result = extract_skills(test_input2, test_dict)

    expected = []

    assert result == expected


def test_extracts_from_full_description():
    test_input = 'Students will create two websites (a 1-page website and a 5-page website) over the course of 12 weeks. Students will learn to code in HTML, CSS and Javascript. Students will experience the following: \r\n\r\n-Discover FTP (File Transfer Process) website servers\r\n-Develop link building skills\r\n-Learn the Bootstrap framework for responsive design\r\n-Learn how to font with Awesome icons\r\n-Learn how to use Photoshop\r\n-Learn how to implement contact forms.'

    result = extract_skills(test_input, test_dict)

    expected = ['HTML', 'CSS', 'Javascript', 'Bootstrap']

    assert sorted(result) == sorted(expected)


def test_ignores_negated_skills_in_full_description():
    test_input = 'Students will create two websites (a 1-page website and a 5-page website) over the course of 12 weeks. Students will learn to code in HTML, CSS and Javascript. Students will experience the following: \r\n\r\n-Discover FTP (File Transfer Process) website servers\r\n-Develop link building skills\r\n-Learn the Bootstrap framework for responsive design\r\n-Learn how to font with Awesome icons\r\n-Learn how to use Photoshop\r\n-Learn how to implement contact forms. We do not teach Python, React, or Ruby on Rails'

    result = extract_skills(test_input, test_dict)

    expected = ['HTML', 'CSS', 'Javascript', 'Bootstrap']

    assert sorted(result) == sorted(expected)


def test_ignores_skills_when_used_as_verbs():
    test_input = "Students should react to danger"

    result = extract_skills(test_input, test_dict)

    assert result == []


def test_picks_skills_when_present_as_verb_and_noun():
    test_input = "Students will learn how use reactjs and React when attacked by hippopotamuses and how to react in danger"

    result = extract_skills(test_input, test_dict)

    assert result == ["reactjs", "React"]


def test_agile_is_always_extracted_as_a_skill():
    test_input = "Students will learn agile practices"

    result = extract_skills(test_input, test_dict)

    assert result == ["agile"]


def test_detects_hyphenation():
    test_input = 'Students will create two websites (a 1-page website and a 5-page website) over the course of 12 weeks. Students will learn to code in HTML, CSS and Javascript. Students will experience the following: \r\n\r\n-Discover FTP (File Transfer Process) website servers\r\n-Develop link building skills\r\n-Learn the Bootstrap framework for responsive design\r\n-Learn how to font with Awesome icons\r\n-Learn how to use Photoshop\r\n-Learn how to implement contact forms. We do not teach Python, React, or Ruby on Rails. We teach Object-oriented programming'

    result = extract_skills(test_input, test_dict)

    expected = ['HTML', 'CSS', 'Javascript', 'Bootstrap', 'Object-oriented programming']

    assert sorted(result) == sorted(expected)
