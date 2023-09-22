from scrapy.crawler import CrawlerProcess
import scrapy
import logging
import re


class DallasUniversityScraper(scrapy.Spider):
    name = 'dallas-college'

    def start_requests(self):
        url = 'http://catalog.untdallas.edu/content.php?catoid=25&navoid=2027'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for uri in response.xpath("//a[contains(@href, 'preview_course')]/@href").getall():
            yield response.follow(uri, callback=self.parse_course)

        next_page_url = response.xpath("//td[text()='Page: ']/span[@aria-current]/following-sibling::a/@href").get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_course(self, response):
        item = {}
        item['code'] = response.xpath("//h1[@id='course_preview_title']/text()").re_first(r'(.*\d{3,6}.*?)(?:-)',
                                                                                          '').strip()
        item['title'] = response.xpath("//h1[@id='course_preview_title']/text()").re_first(r'(?:.*\d{3,6}.*?)(?:-)(.*)',
                                                                                           '').strip()

        

        # Extracting credit hours
        item['credit'] = response.xpath("//strong[contains(text(), 'Credit hours:')]/following-sibling::text()[1]").get().strip()
        # Extracting description
        description = response.xpath("//p/strong[contains(text(), 'Description:')]/following-sibling::text()[1]").get()
        item['description'] = self.normalize_spaces_and_line_breaks(description) if description else ''

    

        yield item

    @staticmethod
    def normalize_spaces_and_line_breaks(text):
        # Replace line breaks with space
        text = text.replace('\n', ' ')

        # Replace multiple spaces with a single space
        text = ' '.join(text.split())

        return text


crawler = CrawlerProcess(settings={
    "FEEDS": {"output/dallas-college.csv": {"encoding": "utf8", "format": "csv", "overwrite": True}},
    "LOG_LEVEL": logging.DEBUG
})
crawler.crawl(DallasUniversityScraper)
crawler.start(stop_after_crawl=True)