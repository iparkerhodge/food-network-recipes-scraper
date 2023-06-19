import scrapy
from food_network.items import FoodNetworkRecipe
from scrapy_splash import SplashRequest

class RecipesSpider(scrapy.Spider):
    name = "recipes"
    allowed_domains = ["www.foodnetwork.com"]

    def start_requests(self):
        url = "https://www.foodnetwork.com/recipes/recipes-a-z/123"
        yield SplashRequest(url, callback=self.parse_tab, args={'wait': 0.5})

    def parse(self, response):
        # links for the tabs "123", "A", "B", "C"...
        all_alphabet_tab_links = response.xpath(".//ul[@class='o-IndexPagination__m-List']/li/a/@href").extract()
        for tab in all_alphabet_tab_links:
            if tab == "//www.foodnetwork.com/recipes/recipes-a-z/123": continue # starts here, so don't repeat

            yield SplashRequest(url=f"https:{tab}", callback=self.parse_tab)

    def parse_tab(self, response):
        links_to_recipes_on_page = response.xpath(".//div[@class='l-Columns l-Columns--2up']/ul/li/a/@href").extract()
        for link in links_to_recipes_on_page:
            url = f'https:{link}'
            yield SplashRequest(url, callback=self.parse_recipe, args={'wait': 1.5})

        next_page = response.xpath(".//a[contains(@class, 'o-Pagination__a-NextButton')][not(contains(@class, 'is-Disabled'))]/@href").extract_first()
        if next_page:
            yield SplashRequest(url=f"https:{next_page}", callback=self.parse_tab)
        pass

    def parse_recipe(self, response):
        recipe = FoodNetworkRecipe()
        # Title
        recipe['title'] = response.xpath(".//h1/span[@class='o-AssetTitle__a-HeadlineText']/text()").extract_first()

        # Ingredients
        recipe['ingredients'] = []
        for ingredient in response.xpath(".//span[@class='o-Ingredients__a-Ingredient--CheckboxLabel']/text()").extract():
            if ingredient != 'Deselect All': recipe['ingredients'].append(" ".join(ingredient.split()))

        # Directions
        recipe['directions'] = []
        directions_list = response.xpath(".//li[@class='o-Method__m-Step']/text()").extract()
        for direction in directions_list:
            formatted_direction = " ".join(direction.replace("\n", "").strip().split())
            recipe['directions'].append(formatted_direction)

        # Categories
        recipe['categories'] = []
        for category in response.xpath(".//a[@class='o-Capsule__a-Tag a-Tag']/text()").extract():
            recipe['categories'].append(" ".join(category.split()))
        
        # Author
        attribution_spans = response.xpath(".//span[@class='o-Attribution__a-Name']")
        if attribution_spans:
            author_span = attribution_spans[0]
            if author_span.xpath(".//a/text()").extract_first():
                recipe['author'] = author_span.xpath(".//a/text()").extract_first()
                recipe['author_profile'] = author_span.xpath(".//a/@href").extract_first()
            else:
                full_string = author_span.xpath(".//text()").extract_first()
                recipe['author'] = " ".join(full_string.split()).replace('RECIPE COURTESY OF ', '').replace('Recipe courtesy of ', '')
        else:
            recipe['author'] = None

        # Level - Easy, Hard, etc.
        recipe["level"] = response.xpath(".//ul[@class='o-RecipeInfo__m-Level']/li/span[@class='o-RecipeInfo__a-Description']/text()").extract_first()

        # Time (total and active)
        time_ul = response.xpath(".//ul[@class='o-RecipeInfo__m-Time']")

        recipe['total_time'] = time_ul.xpath(".//li/span[@class='o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total']/text()").extract_first()
        recipe['active_time'] = time_ul.xpath(".//li[2]/span[@class='o-RecipeInfo__a-Description']/text()").extract_first()

        # Servings
        recipe['servings'] = response.xpath(".//ul[@class='o-RecipeInfo__m-Yield']/li[1]/span[@class='o-RecipeInfo__a-Description']/text()").extract_first()

        # Image
        src = response.xpath(".//section[contains(@class, 'o-RecipeLead')]/div/div/div/img[@class='m-MediaBlock__a-Image a-Image']/@src").extract_first()
        if src: recipe['image_url'] = f"https:{src}"

        print(recipe)
        yield recipe