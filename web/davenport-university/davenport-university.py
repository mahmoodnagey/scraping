from scrapy.crawler import CrawlerProcess
import scrapy
import logging
import re


class DavenportUniversityScraper(scrapy.Spider):
    name = 'davenport-university'

    def start_requests(self):
        url = 'https://catalog.davenport.edu/content.php?filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=3&expand=&navoid=86&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter'
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

        strong_texts = response.css("td[class='block_content'] strong::text").getall()

        # Extracting credit hours
        for i, text in enumerate(strong_texts):
            if text.strip() == "Credits" and i > 0:
                item['credit'] = strong_texts[i - 1].strip()  # The preceding text should be the credit hours
                break

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
            item['description'] = ''

        yield item

    @staticmethod
    def normalize_spaces_and_line_breaks(text):
        # Replace line breaks with space
        text = text.replace('\n', ' ')

        # Replace multiple spaces with a single space
        text = ' '.join(text.split())

        return text


crawler = CrawlerProcess(settings={
    "FEEDS": {"output/davenport-university.csv": {"encoding": "utf8", "format": "csv", "overwrite": True}},
    "LOG_LEVEL": logging.DEBUG
})
crawler.crawl(DavenportUniversityScraper)
crawler.start(stop_after_crawl=True)