from .app import collector_adzuna
from azure.functions import TimerRequest, InputStream, Out


def main(mytimer: TimerRequest, inBlob: InputStream, outBlob: Out[bytes]) -> None:
    """Main function of collector_adzuna

    :param mytimer: Azure timer trigger
    :type mytimer: TimerRequest
    :param inBlob: Azure input blob
    :type inBlob: InputStream
    :param outBlob: Azure output blob
    :type outBlob: Out[bytes]
    """
    api_data = collector_adzuna(inBlob)

    outBlob.set(api_data.encode('utf-8'))
