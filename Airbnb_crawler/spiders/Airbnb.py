import scrapy
import numpy as np

description = "__tutorial__"
author = "__Gabriel__"
contact = "__gabrielyin@berkeley.edu"

class Crawler(scrapy.Spider):
    # class name definition
    name = "web_crawler"

    def start_requests(self):
        # define urls to be crawled
        URL = "https://www.airbnb.com/s/New-York--NY--United-States/all?refinement_paths%5B%5D=%2Ffor_you&query=New%20York%2C%20NY%2C%20United%20States&place_id=ChIJOwg_06VPwokRYv534QaPC8g"
        yield scrapy.Request(url=URL , callback=self.parse)

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


class Airbnb(scrapy.Spider):
    # airbnb crawler
    name = "airbnb_crawler"

    def start_requests(self):
        URL = "https://www.airbnb.com/rooms/20532901?location=New%20York%2C%20NY%2C%20United%20States&adults=1&children=0&infants=0&guests=1&check_in=2018-10-04&check_out=2018-10-16&s=90kv0Krj"
        yield scrapy.Request(url=URL , callback=self.parse)

    def parse(self, response):
        # type of the room
        type = response.css('span[class="_1hh2h7tb"] span::text').extract_first()
        # title of the room
        title = response.css('h1[class="_1xu9tpch"]::text').extract_first()
        # '1 bedroom' '2 private baths' '3 beds' '5 guests'
        infos = np.array(response.xpath("//span[@class = '_fgdupie']/text()").extract()[:4])
        # print(len(infos), infos)
        guests = infos[0].split(' ')[0]
        bedroom = infos[1].split(' ')[0]
        beds = infos[2].split(' ')[0]
        baths = infos[3].split(' ')[0]
        # yield json result
        yield {
              'type' : type,
              'title' : title,
              'guests' : guests,
              'bedroom' : bedroom,
              'beds' : beds,
              'baths' : baths
        }
