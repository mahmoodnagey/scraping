from scrapy.crawler import CrawlerProcess
import scrapy
import logging
import re


class IndianaStateUniversityScraper(scrapy.Spider):
    name = 'indiana-state-university'

    def start_requests(self):
        url = 'https://catalog.indstate.edu/content.php?filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=56&expand=&navoid=2801&search_database=Filter#acalog_template_course_filter'
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

        text_items = response.css("td[class='block_content']::text")

        possible_desc = []
        for text_item in text_items:
            if 'Credits' in text_item.get():
                item['credit'] = text_item.re_first('.*').replace('Credits', '').replace('Variable', '').strip()

            elif len(text_item.get()) >= 100:
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
    "FEEDS": {"output/indiana-state-university.csv": {"encoding": "utf8", "format": "csv", "overwrite": True}},
    "LOG_LEVEL": logging.DEBUG
})
crawler.crawl(IndianaStateUniversityScraper)
crawler.start(stop_after_crawl=True)