import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_skills(description):

    technologies = 'JavaScript, Front-End'

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'Extract a single, comma separated list of technologies, programming languages, and frameworks from the following description where the course purports to teach this :\n\n """{description}""" \n which are similar to or equal to these examples: \n """{technologies}""" ',
        max_tokens=100,
        top_p=0.1,
        temperature=1,
        frequency_penalty=0.8,
        presence_penalty=0.0
    )

    output = response.choices[0].text.strip()

    print('OUTPUT', output)

    return output.split(', ')
