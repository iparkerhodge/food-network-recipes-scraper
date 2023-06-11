import scrapy
from food_network.items import FoodNetworkRecipe
from scrapy_splash import SplashRequest

class RecipesSpider(scrapy.Spider):
    name = "recipes"
    allowed_domains = ["www.foodnetwork.com"]

    def start_requests(self):
        url = "https://www.foodnetwork.com/recipes/recipes-a-z/123"
        yield SplashRequest(url, callback=self.parse, args={'wait': 0.5})

    def parse(self, response):
        # links for the tabs "123", "A", "B", "C"...
        # ignore for now, just try and get recipes on first tab
        # all_alphabet_tab_links = response.xpath(".//ul[@class='o-IndexPagination__m-List']/li/a/@href").extract()

        links_to_recipes_on_page = response.xpath(".//div[@class='l-Columns l-Columns--2up']/ul/li/a/@href").extract()
        for link in links_to_recipes_on_page:
            # link formatted as: "//www.foodnetwork.com/recipes/ina-garten/16-bean-pasta-e-fagioli-3612570"
            url = f'https:{link}'
            yield SplashRequest(url, callback=self.parse_recipe, args={'wait': 1.5})

        pass

    def parse_recipe(self, response):
        recipe = FoodNetworkRecipe()
        # Title
        recipe['title'] = response.xpath(".//h1/span[@class='o-AssetTitle__a-HeadlineText']/text()").extract_first()

        # Ingredients
        recipe['ingredients'] = []
        for ingredient in response.xpath(".//span[@class='o-Ingredients__a-Ingredient--CheckboxLabel']/text()").extract():
            if ingredient != 'Deselect All': recipe['ingredients'].append(ingredient)
        
        # Author
        # recipe['author'] = response.xpath(".//div[@class='o-Attribution__m-Author']/span[@class='o-Attribution__a-Author--Prefix']/span[@class='o-Attribution__a-Name']/a/text()").extract_first()
        author_span = response.xpath(".//span[@class='o-Attribution__a-Name']")[0]
        if author_span:
            if author_span.xpath(".//a/text()").extract_first():
                recipe['author'] = author_span.xpath(".//a/text()").extract_first()
            else:
                full_string = author_span.xpath(".//text()").extract_first()
                recipe['author'] = " ".join(full_string.split()).replace('RECIPE COURTESY OF ', '').replace('Recipe courtesy of ', '')
        else:
            recipe['author'] = None
        print(recipe)
        yield recipe