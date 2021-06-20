import scrapy
from bangumi.spiders.bangumi_list import BangumiListSpider


class BangumiAnimeListSpider(BangumiListSpider):
	name = 'bangumi_anime_list'
	type = 'anime'
	start_page = 1

