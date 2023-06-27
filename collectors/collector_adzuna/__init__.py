from .app import collector_adzuna
from azure.functions import TimerRequest, InputStream, Out


def main(mytimer: TimerRequest, inSkillsDict: InputStream, outAdzunaJobCounts: Out[bytes]) -> None:
    """Main function of collector_adzuna

    :param mytimer: Azure timer trigger
    :type mytimer: TimerRequest
    :param inSkillsDict: Azure input blob
    :type inSkillsDict: InputStream
    :param outAdzunaJobCounts: Azure output blob
    :type outAdzunaJobCounts: Out[bytes]
    """
    api_data = collector_adzuna(inSkillsDict)

    outAdzunaJobCounts.set(api_data.encode('utf-8'))
