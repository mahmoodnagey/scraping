from scrapy.crawler import CrawlerProcess
import scrapy
import logging
import re


class BrazosportCollegeScraper(scrapy.Spider):
    name = 'brazosport-college'

    def start_requests(self):
        url = 'https://catalog.brazosport.edu/content.php?catoid=28&navoid=4703'
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

        item['credit'] = item['code'][6]
        # Extracting description
        text_items = response.css("td[class='block_content']::text")

        possible_desc = []
        for text_item in text_items:
            if len(text_item.get()) >= 100:
                desc = self.normalize_spaces_and_line_breaks(text_item.get().strip())
                length = len(text_item.get())
                possible_desc.append((length, desc))

        possible_desc.sort()
        if len(possible_desc) >= 1:
            item['description'] = possible_desc[-1][1]
        else:
            description = self.normalize_spaces_and_line_breaks(response.xpath("//td[@class='block_content']//strong[text()='Credit Hours:']/following-sibling::text()[2]").get().strip())
            if description:
                item['description'] = description
            else:
                description = self.normalize_spaces_and_line_breaks(response.xpath("//td[@class='block_content']//strong[text()='Credit Hours:']/following-sibling::text()[1]").get().strip())
        yield item

    @staticmethod
    def normalize_spaces_and_line_breaks(text):
        # Replace line breaks with space
        text = text.replace('\n', ' ')

        # Replace multiple spaces with a single space
        text = ' '.join(text.split())

        return text


crawler = CrawlerProcess(settings={
    "FEEDS": {"output/brazosport-college.csv": {"encoding": "utf8", "format": "csv", "overwrite": True}},
    "LOG_LEVEL": logging.DEBUG
})
crawler.crawl(BrazosportCollegeScraper)
crawler.start(stop_after_crawl=True)