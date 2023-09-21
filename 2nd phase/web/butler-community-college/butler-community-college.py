from scrapy.crawler import CrawlerProcess
import scrapy
import logging
import re
from scrapy.exporters import CsvItemExporter

class ButlerCommunityCollegeScraper(scrapy.Spider):
    name = 'butler-community-college'

    def start_requests(self):
        url = 'https://catalog.butlercc.edu/content.php?catoid=10&navoid=485'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for uri in response.xpath("//a[contains(@href, 'preview_course')]/@href").getall():
            yield response.follow(uri, callback=self.parse_course)

        next_page_url = response.xpath("//td[text()='Page: ']/span[@aria-current]/following-sibling::a/@href").get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_course(self, response):
        item = {}
        item['code'] = response.xpath("//h1[@id='course_preview_title']/text()").re_first(r'(\b[A-Z]+\s+\d{2,4}-?\d*)')

        title_text = response.xpath("//h1[@id='course_preview_title']/text()").get()

        title_match = re.search(r'\b[A-Z]+\s+\d{2,4}-?\d*\.\s*(.*)', title_text)
        if title_match:
            item['title'] = title_match.group(1)
        else:
            item['title'] = None

        # Extracting description
        text_items = response.css("td[class='block_content']::text")

        possible_desc = []

        for text_item in text_items:
            text = text_item.get().strip()  # Get the text content and remove leading/trailing spaces

            # Check if the text contains a numeric value (assuming course credits are numeric)
            if text.isdigit():
                item['credit'] = int(text)  # Convert the numeric text to an integer
            elif "Credits:" in text:
                # Extract credit information after "Credits:"
                credit_match = re.search(r"Credits:\s*([\d.]+)", text)
                if credit_match:
                    item['credit'] = float(credit_match.group(1))
                else:
                    item['credit'] = 0
            elif len(text) >= 100:
                desc = self.normalize_spaces_and_line_breaks(text)
                length = len(text)
                possible_desc.append((length, desc))
                possible_desc.sort()
        if len(possible_desc) >= 1:
            item['description'] = possible_desc[-1][1]
        else:
            item['description'] = ''

        # Handling courses followed by "-0"
        if "-0" in item['code']:
            item['code'] = item['code'].replace("-0", "")

        print(item['credit'])
        yield item

    @staticmethod
    def normalize_spaces_and_line_breaks(text):
        # Replace line breaks with space
        text = text.replace('\n', ' ')

        # Replace multiple spaces with a single space
        text = ' '.join(text.split())

        return text


crawler = CrawlerProcess(settings={
    "LOG_LEVEL": logging.DEBUG,
    "FEEDS": {"output/butler-community-college.csv": {"format": "csv"}},
    "FEED_EXPORTERS": {
        'csv': 'scrapy.exporters.CsvItemExporter',
    }
})
crawler.crawl(ButlerCommunityCollegeScraper)
crawler.start()