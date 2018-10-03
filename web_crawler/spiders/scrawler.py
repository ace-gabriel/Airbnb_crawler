import scrapy

description = "__tutorial__"
author = "__Gabriel__"
contact = "__gabrielyin@berkeley.edu"

class Crawler(scrapy.Spider):
    # class name definition
    name = "web_crawler"

    def start_requests(self):
        # define urls to be crawled
        urls = [
        'http://quotes.toscrape.com/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_info(self, response):
        # store two files, quotes-1.html quotes-2.html
        page = response.url.split("/")[-2]
        filename = 'quotes-%s' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file.')
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
        start_urls = [
        'http://quotes.toscrape.com/page/1/',]

    def parse(self, response):
        print("URL", response.url)
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        print(next_page + 'relative')
        if next_page is not None:
            next_page = response.urljoin(next_page)

            print(next_page + 'absolute')
            yield scrapy.Request(next_page, callback=self.parse)
