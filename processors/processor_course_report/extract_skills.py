import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_skills(description):

    technologies = 'JavaScript, Front End'

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'Extract a list of programming skills, technologies and frameworks from the following description:\n\n """{description}""" \n which are similar to or equal to these example technologies: \n """{technologies}""" ',
        temperature=1,
        max_tokens=100,
        top_p=0.1,
        frequency_penalty=0.8,
        presence_penalty=0.0
    )

    output = response.choices[0].text

    print('OUTPUT', output)

    return output.split('\n-')
