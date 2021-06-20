import scrapy
from bangumi.spiders.bangumi_list import BangumiListSpider


class BangumiMusicListSpider(BangumiListSpider):
	name = 'bangumi_music_list'
	type = 'music'
	start_page = 1

