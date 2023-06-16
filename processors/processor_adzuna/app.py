import csv
import json
import io
from azure.functions import InputStream


def process_adzuna_data(inBlob: InputStream):
    """Generates a csv file based on json data from adzuna

    :param inBlob: an azure input stream containing raw blob data
    :type inBlob: InputStream
    :raises Exception: empty blob alert
    :return: a csv representation of the raw json data
    :rtype: StringIO
    """

    input_json = inBlob.read().decode('utf-8')

    if input_json == '':
        raise Exception('Blob is empty, check json output from collector')

    parsed_input = json.loads(input_json)

    error_handling(parsed_input)

    csv_file = io.StringIO()
    csvwriter = csv.writer(csv_file, delimiter=',')
    csvwriter.writerow(['skill', 'number_of_jobs'])
    for key in parsed_input:
        csvwriter.writerow([key, parsed_input[key]])

    return csv_file


def error_handling(parsed_input):
    """Error Handling for process_adzuna_data

    :param parsed_input: parsed json input
    :type parsed_input: json
    :raises Exception: Empty unprocessed json
    :raises Exception: Skill value incorrect
    """

    if len(parsed_input) == 0:
        raise Exception(
            'Unprocessed json is empty, check json output from collector')

    for skill_count in parsed_input.values():
        if type(skill_count) != int:
            raise Exception(
                'At least one of the skills count values is not an integer')
