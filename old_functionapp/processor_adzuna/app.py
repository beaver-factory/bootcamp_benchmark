import csv
import json
import io


def process_adzuna_data(inBlob):
    """
    Takes the raw json produced by collector_adzuna and returns a csv file
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
    """
    Checks the input given to process_adzuna_data and raises Exceptions if needed
    """

    if len(parsed_input) == 0:
        raise Exception('Unprocessed json is empty, check json output from collector')

    for skill_count in parsed_input.values():
        if type(skill_count) != int:
            raise Exception('At least one of the skills count values is not an integer')
