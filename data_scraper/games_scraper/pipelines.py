# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class GamesScraperPipeline:
    def __init__(self):
        self.file = open("nba_odds.json", "w")


    def process_item(self, item, spider):
        if item["bookmakers"] and item["odds"]:
            item["odds_by_house"]= {i[0]:(i[1], i[2]) for i in list(zip(item["bookmakers"], [i for i in item["odds"][0::2]], [i for i in item["odds"][1::2]]))}
            
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
    
    def close_spider(self, spider):
        self.file.close()
