from .spider import CourseReportSpider
from scrapyscript import Job, Processor


def get_scraped_data():
    """
    Executes and retrieves output from CourseReportSpider

    :return: list of skill provider objects
    :rtype: list
    """
    processor = Processor()
    job = Job(CourseReportSpider)
    results = processor.run(job)
    return results
