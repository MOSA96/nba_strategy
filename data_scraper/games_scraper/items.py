# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GamesScraperItem(scrapy.Item):
    season = scrapy.Field()
    date = scrapy.Field()
    local_team = scrapy.Field()
    local_points = scrapy.Field()
    visit_team = scrapy.Field()
    visit_points = scrapy.Field()
    bookmakers = scrapy.Field()
    odds = scrapy.Field()
    odds_by_house = scrapy.Field()
