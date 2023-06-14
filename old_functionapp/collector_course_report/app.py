from .spider import CourseReportSpider
from scrapyscript import Job, Processor


def get_scraped_data():
    """
    Returns the output from the execution of CourseReportSpider as list of providers
    """
    processor = Processor()
    job = Job(CourseReportSpider)
    results = processor.run(job)
    return results
