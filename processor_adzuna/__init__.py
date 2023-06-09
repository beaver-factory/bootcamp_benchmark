from .app import process_adzuna_data

import azure.functions as func


def main(inBlob: func.InputStream, outBlob: func.Out[bytes]) -> None:
    csv_file = process_adzuna_data(inBlob)

    outBlob.set(csv_file.close())
    # csv_file.close()
