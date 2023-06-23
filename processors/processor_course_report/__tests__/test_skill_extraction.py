from ..extract_skills import extract_skills
import pytest

test_input = "As a Software Engineer graduate you will be ready to start a career in a variety of coding roles. Throughout this bootcamp you will learn to: create front-end web application with modern JavaScript frameworks such as Angular or React, develop full-stack applications with in-demand technologies such as Ruby on Rails, Python with Django, and Express with Node.js, and integrate third-party application programming interfaces (APIs) in an application."

test_input2 = "Become a software engineer in 13 weeks at our coding bootcamps in Manchester, Leeds, Newcastle, Birmingham and remotely. Unlike our Data Engineering bootcamp where you focus specifically on the 'back-end' of software, or our DevOps Engineering bootcamp that deals specifically with software development and IT operations, our coding bootcamp focuses on building websites and mobile phone apps. The application process takes 2-3 weeks and we would advise you to apply sooner rather than later to give yourself plenty of time to work through the preparation materials. Applicants living in England can apply for DfE funding to cover the entire cost of the course. Get in touch to find out if you qualify."

test_input3 = "As a Data Analyst graduate you will be able to problem solve and effectively communicate like an analyst. This course teaches you to use industry-standard tools to make ethical, data-driven decisions. Experience hands-on training to master SQL, Excel, Tableau, PowerBI, and Python – tools listed in virtually every data analytics job posting across industries."

test_input4 = "The course is designed for everyone, whether a complete novice, a computer science graduate wanting practical experience, or an entrepreneur sick of looking for a technical co-founder. Students learn an incredible amount, including: Ruby on Rails; HTML5 and CSS3; time management; communication skills; customer service; Agile and Lean Development; JavaScript, jQuery and NodeJS; along with Git and Heroku, and software design best practices. Students learn through first hand experience, community-driven classrooms, pairing, and project-based work."

test_input5 = "On our Data Science course, you will learn the fundamentals of this discipline, including Python, how to make dashboards using PowerBI, database management and PSQL. We do not cover JavaScript, Front End nor how to make a website using HTML."


def test_returns_correct_typing():
    result = extract_skills(test_input)

    for skill in result:
        assert type(skill) is str


def test_returns_expected_list_of_skills():
    result = extract_skills(test_input)

    expected = ['JavaScript', 'Angular', 'React', 'Ruby on Rails', 'Python', 'Django', 'Express', 'Node.js']

    assert result == expected


def test_raises_exception_on_incorrect_input_type():
    with pytest.raises(Exception) as e:
        extract_skills(123)

    assert str(e.value) == 'Input must be str'
