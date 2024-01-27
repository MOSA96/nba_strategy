import scrapy
from scrapy.http import Request
from scrapy_playwright.page import PageMethod
from games_scraper.items import GamesScraperItem

scrolling_script = """
    const scrolls = 8
    let scrollCount = 0
    
    // scroll down and then wait for 0.5s
    const scrollInterval = setInterval(() => {
      window.scrollTo(0, document.body.scrollHeight)
      scrollCount++
    
      if (scrollCount === numScrolls) {
        clearInterval(scrollInterval)
      }
    }, 500)
    """

class GamesSpider(scrapy.Spider):
    name = "games"
    allowed_domains = ["www.oddsportal.com"]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        start_urls = [f"https://www.oddsportal.com/basketball/usa/nba-2022-2023/results/#/page/{page_number}" for page_number in range(1,29)]
        for url in start_urls:
            yield scrapy.Request(url, 
                                 callback=self.parse, 
                                 dont_filter = True,
                                 meta={"playwright": True,
                                        "playwright_page_methods": [
                                        PageMethod("evaluate", scrolling_script),
                                        PageMethod("wait_for_timeout", 10000)
                                        ],})


    def parse(self, response):
        game_links = {}
        item = GamesScraperItem()
        item["season"] = response.xpath("//a[@class='flex items-center justify-center h-8 px-3 bg-gray-medium cursor-pointer active-item-calendar']/text()").get()
        game_dates = response.xpath("//div[@class='eventRow flex w-full flex-col text-xs']").getall()
        next_page = response.xpath("//div[@class='pagination my-7 flex items-center justify-center']/a[@class='pagination-link']")
        for game_date in game_dates:
            game_date = scrapy.Selector(text=game_date)
            if game_date.xpath("//div[@class='border-black-borders bg-gray-light flex w-full min-w-0 border-l border-r']"):
                date = game_date.xpath("//div[@class='border-black-borders bg-gray-light flex w-full min-w-0 border-l border-r']/div[@class='border-black-borders flex w-full min-w-0 items-center justify-start pl-2']/div[@class='text-black-main font-main w-full truncate text-xs font-normal leading-5']/text()").get()
                game_link = game_date.xpath("//div[@class='flex w-full items-center']/div[@class='align-center mx-1 flex w-full flex-col items-center gap-1']/div[@class='max-mt:pl-1 flex w-full flex-col gap-1 pt-[2px] text-xs leading-[16px] min-mt:!flex-row min-mt:!gap-2 justify-center']/a[@class='min-mt:!justify-end flex basis-[50%] cursor-pointer items-start justify-start gap-1 overflow-hidden']/@href").get()
                game_links[date] = [game_link]
            else: 
                game_link = game_date.xpath("//div[@class='flex w-full items-center']/div[@class='align-center mx-1 flex w-full flex-col items-center gap-1']/div[@class='max-mt:pl-1 flex w-full flex-col gap-1 pt-[2px] text-xs leading-[16px] min-mt:!flex-row min-mt:!gap-2 justify-center']/a[@class='min-mt:!justify-end flex basis-[50%] cursor-pointer items-start justify-start gap-1 overflow-hidden']/@href").get()
                game_links[date].append(game_link)
        
        for game in game_links.keys():
            for game_url in game_links[game]:
                base_url = "https://www.oddsportal.com"
                complete_url = base_url + game_url
                yield scrapy.Request(complete_url, 
                                    callback=self.parse_games,
                                    meta={"playwright": True,
                                          'date':game,
                                            "playwright_page_methods": [
                                            PageMethod("evaluate", scrolling_script),
                                            PageMethod("wait_for_timeout", 5000),
                                            ],})


    def parse_games(self, response):
        item = GamesScraperItem()
        item["date"] = response.meta.get("date")
        item["local_team"] = response.xpath("//div[@class='relative px-[12px] flex max-mm:flex-col w-auto min-sm:w-full pb-5 pt-5 min-mm:items-center font-semibold text-[22px] text-black-main gap-2 border-b border-black-borders font-secondary']/div[@class='flex items-center gap-1 min-sm:gap-2 min-mm:flex-row justify-content']/div[@class='flex justify-between w-full gap-1 min-mm:gap-2']/div[@class='flex items-center gap-1 min-mm:gap-2 max-mm:truncate !justify-between']/span/text()").get()
        item['local_points'] = response.xpath("//div[@class='relative px-[12px] flex max-mm:flex-col w-auto min-sm:w-full pb-5 pt-5 min-mm:items-center font-semibold text-[22px] text-black-main gap-2 border-b border-black-borders font-secondary']/div[@class='flex items-center gap-1 min-sm:gap-2 min-mm:flex-row justify-content']/div[@class='flex justify-between w-full gap-1 min-mm:gap-2']/div[@class='flex items-center justify-end max-mm:gap-2']/div/text()").get()
        item['visit_team'] = response.xpath("//div[@class='relative px-[12px] flex max-mm:flex-col w-auto min-sm:w-full pb-5 pt-5 min-mm:items-center font-semibold text-[22px] text-black-main gap-2 border-b border-black-borders font-secondary']/div[@class='flex items-center gap-1 min-mm:gap-2 max-mm:justify-between max-mm:w-full']/div[@class='flex-center items-center gap-1 min-mm:gap-2 justify-content max-mm:truncate']/span/text()").get()
        item['visit_points'] = response.xpath("//div[@class='relative px-[12px] flex max-mm:flex-col w-auto min-sm:w-full pb-5 pt-5 min-mm:items-center font-semibold text-[22px] text-black-main gap-2 border-b border-black-borders font-secondary']/div[@class='flex items-center gap-1 min-mm:gap-2 max-mm:justify-between max-mm:w-full']/div[@class='flex order-first max-mm:order-last max-mm:gap-2']/div/text()").get()
        item['bookmakers'] = response.xpath("//div[@class='border-black-borders flex h-9 border-b border-l border-r text-xs']/div[@class='max-ms:!justify-center flex w-full items-center justify-start max-sm:flex-wrap max-sm:gap-1 border-[#E0E0E0]']/a[@target='_blank']/p/text()").getall()
        item['odds'] = response.xpath("//div[@class='border-black-borders flex h-9 border-b border-l border-r text-xs']/div/div[@class='flex-center flex-col font-bold text-[#2F2F2F]']/div[@class='flex flex-row items-center gap-[3px]']/p[@class='height-content']/text()").getall()
        yield item