from .app import collector_adzuna
import azure.functions as func


def main(mytimer: func.TimerRequest, inBlob: func.InputStream, outBlob: func.Out[bytes]) -> None:
    api_data = collector_adzuna(inBlob)

    outBlob.set(api_data.encode('utf-8'))
