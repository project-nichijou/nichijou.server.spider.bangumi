import scrapy
from bangumi.spiders.bangumi_list_spider import BangumiListSpider


class BangumiAnimeListSpider(BangumiListSpider):

	name = 'bangumi_anime_list'
	type = 'anime'
	start_page = 1
