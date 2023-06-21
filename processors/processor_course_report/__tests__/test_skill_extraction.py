from ..extract_skills import extract_skills


def test_returns_correct_typing():
    test_input = "As a Software Engineer graduate you will be ready to start a career in a variety of coding roles. Throughout this bootcamp you will learn to: create front-end web application with modern JavaScript frameworks such as Angular or React, develop full-stack applications with in-demand technologies such as Ruby on Rails, Python with Django, and Express with Node.js, and integrate third-party application programming interfaces (APIs) in an application."
    result = extract_skills(test_input)

    print('RESULT', result)

    for skill in result:
        assert type(skill) is str
