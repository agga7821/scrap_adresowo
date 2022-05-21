import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from ..items import ApartmentItem


class AdresowoSpider(scrapy.Spider):
    name = "adresowo"

    handle_httpstatus_list = [302]

    start_urls = [
        "https://adresowo.pl/mieszkania/krakow/",
        # "https://adresowo.pl/domy/krakow/",
        # "https://adresowo.pl/dzialki/krakow/"
    ]

    max_retries = 3

    def parse(self, response, **kwargs):
        adverts = response.css(".search-results__block > section")
        if response.status in self.handle_httpstatus_list:
            print('Response redirected! Increase delay!')
        for advert in adverts:
            loader = ItemLoader(item=ApartmentItem(), selector=advert)
            loader.default_output_processor = TakeFirst()
            result_basic_containers = advert.css("span.result-info__basic-container > span")
            if not result_basic_containers:  # not an advert
                continue
            loader.add_css("city", "h2.result-info__header > strong::text")
            loader.add_css("district", "h2.result-info__header > strong::text")
            loader.add_css("address", "h2.result-info__header > span.result-info__address::text")
            loader.add_css("property_type", "h2.result-info__header > span.result-info__property-type > b::text")
            loader.add_value("rooms", result_basic_containers[0].css("b::text").get())
            loader.add_value("squares", result_basic_containers[1].css("b::text").get())
            loader.add_value("floor", result_basic_containers[2].css("b::text").get())
            loader.add_css("directly", "span.result-info__basic--owner::text")
            loader.add_css("price", "div.result-info__price--total > span::text")
            loader.add_css("price_per_square", "div.result-info__price--per-sqm > span::text")
            loader.add_css("description", "p.result-info__description::text")
            link = advert.css("div.result-info > a::attr(href)").get()
            loader.add_value("link", response.urljoin(link))
            yield loader.load_item()
        next_page = response.css("a.search-pagination__next::attr(href)").get()
        yield scrapy.Request(response.urljoin(next_page), self.parse)
