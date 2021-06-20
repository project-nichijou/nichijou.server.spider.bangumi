import scrapy
from bangumi.spiders.bangumi_list import BangumiListSpider


class BangumiGameListSpider(BangumiListSpider):
	name = 'bangumi_game_list'
	type = 'game'
	start_page = 1

