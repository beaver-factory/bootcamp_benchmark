from .spider import CourseReportSpider
from scrapyscript import Job, Processor


def get_scraped_data():
    processor = Processor()
    job = Job(CourseReportSpider)
    results = processor.run(job)
    return results
