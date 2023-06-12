from scrapy.item import Item, Field


class FoodNetworkRecipe(Item):
    # define the fields for your item here like:
    title = Field()
    author = Field()
    # rating = Field()
    # review_count = Field()
    level = Field()
    total_time = Field()
    active_time = Field()
    # servings = Field()
    # TO DO: get nutrition info
    ingredients = Field()
    directions = Field()
    # note = Field()
    categories = Field()
    # comments = Field()
    pass
