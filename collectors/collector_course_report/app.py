from .spider import CourseReportSpider
from scrapyscript import Job, Processor


def get_scraped_data():
    """
    Executes and retrieves output from CourseReportSpider

        Parameters: none

        Returns:
        - (List[obj]): list of skill provider objects
    """
    processor = Processor()
    job = Job(CourseReportSpider)
    results = processor.run(job)
    return results
