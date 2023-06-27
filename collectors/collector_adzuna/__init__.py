from .app import collector_adzuna
from azure.functions import TimerRequest, InputStream, Out


def main(mytimer: TimerRequest, inLatestSkills: InputStream, inSkillsDict: InputStream, outAdzunaJobCounts: Out[bytes]) -> None:
    """Main function of collector_adzuna

    :param mytimer: Azure timer trigger
    :type mytimer: TimerRequest
    :param inLatestSkills: Azure input blob
    :type inLatestSkills: InputStream
    :param inSkillsDict: Azure input blob
    :type inSkillsDict: InputStream
    :param outAdzunaJobCounts: Azure output blob
    :type outAdzunaJobCounts: Out[bytes]
    """
    api_data = collector_adzuna(inLatestSkills, inSkillsDict)

    outAdzunaJobCounts.set(api_data.encode('utf-8'))
