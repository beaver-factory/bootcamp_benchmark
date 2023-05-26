import scrapy
from datetime import datetime


class CourseReportSpider(scrapy.Spider):
    name = 'course-report-spider'

    start_urls = ['https://www.coursereport.com/cities']
    allowed_domains = ['coursereport.com']

    def parse(self, response):
        if response.url == self.start_urls[0]:
            cities = response.xpath(
                '//li[contains(@data-city-name, "united kingdom")]/a')

            for city in cities:
                yield response.follow(city, self.parse)

        elif 'cities' in response.url:
            schools = response.xpath('//a[contains(@href, "/schools/")]')

            for school in schools:
                yield response.follow(school, self.parse)

        elif 'schools' in response.url:
            provider_name = response.css('h1::text').extract_first()
            provider_locations = response.xpath(
                '//div[contains(text(), "Locations")]/following-sibling::div/a/text()').extract()
            provider_tracks = response.xpath(
                '//div[contains(text(), "Career tracks")]/following-sibling::div/a/text()').extract()

            course_sections = response.xpath(
                '//div[@data-quick-links-section-name="courses"]/div[@data-ga="card"]').extract()

            provider_courses = []

            for course in course_sections:
                course_section_html = scrapy.Selector(text=course)

                course_name = course_section_html.xpath(
                    '//h3[@data-ga="card-title"]/text()').extract_first()
                course_skills = course_section_html.xpath(
                    '//td/a[contains(@href, "/subjects/")]/text()').extract()
                course_locations = course_section_html.xpath(
                    '//td[contains(text(), "Location")]/following-sibling::td/text()').extract_first()
                course_description = course_section_html.xpath(
                    '//p[@data-toggle-target="content"]/text()').extract_first()

                provider_courses.append({
                    "course_name": course_name,
                    "course_skills": course_skills,
                    "course_locations": course_locations,
                    "course_description": course_description
                })

            yield {
                "provider_name": provider_name,
                "provider_locations": provider_locations,
                "provider_tracks": provider_tracks,
                "provider_courses": provider_courses,
                "meta": {
                    "target_url": response.url,
                    "timestamp": f"{datetime.now()}"
                }
            }
