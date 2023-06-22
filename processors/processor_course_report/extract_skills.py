import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_skills(description):
    """
    Runs an openAI API query to return a list of digital skills from a given course description

    :param description: a string detailing what a bootcamp course offers
    :type description: string
    :return: list of digital skills included in the course description
    :rtype: list
    """

    examples = 'JavaScript, Front-End, HTML, CSS, Node.js'

    prompt1 = f'Extract a single, comma separated list of technologies, programming languages, and frameworks from the following description where the course purports to teach this :\n\n """{description}""" \n which are similar to or equal to these examples: \n """{examples}""" '

    # Alternative prompt following prompt writing guidelines, though gave slightly worse results
    # prompt2 = f'''Extract a single, comma separated list of technologies, programming languages, and frameworks from the description below which are similar to or equal to these examples: {examples}

    # ###
    # Description: {description}
    # '''

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt1,
        max_tokens=100,
        top_p=0.1,
        temperature=1,
        frequency_penalty=0.8,
        presence_penalty=0.0
    )

    output = response.choices[0].text.strip()

    return output.split(', ')
