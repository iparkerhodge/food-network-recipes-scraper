import scrapy


class RecipesSpider(scrapy.Spider):
    name = "recipes"
    allowed_domains = ["www.foodnetwork.com"]
    start_urls = ["https://www.foodnetwork.com/recipes/recipes-a-z/123"]

    def parse(self, response):
        pass
