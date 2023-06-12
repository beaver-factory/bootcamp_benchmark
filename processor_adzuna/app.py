import csv
import json
import io


def process_adzuna_data(inBlob):
    input_json = inBlob.read().decode('utf-8')

    parsed_input = json.loads(input_json)

    error_handling(parsed_input)

    csv_file = io.StringIO()
    csvwriter = csv.writer(csv_file, delimiter=',')
    csvwriter.writerow(['skill', 'number_of_jobs'])
    for key in parsed_input:
        csvwriter.writerow([key, parsed_input[key]])

    return csv_file


def error_handling(parsed_input):
    if parsed_input == {}:
        raise Exception('Adzuna raw json is empty')

    for skill_count in parsed_input.values():
        if type(skill_count) != int:
            raise Exception('At least one of the skills count values is not an integer')
