import csv
import json
import io


def process_adzuna_data(inBlob):
    input_json = inBlob.read().decode('utf-8')

    parsed_input = json.loads(input_json)

    csv_file = io.StringIO()
    csvwriter = csv.writer(csv_file, delimiter=',')
    csvwriter.writerow(['skill', 'number_of_jobs'])
    for key in parsed_input:
        csvwriter.writerow([key, parsed_input[key]])

    return csv_file