import scrapy


class BangumiAnimeEpisodeItem(scrapy.Item):
	# episode id
	eid = scrapy.Field()
	# 简介 (HTML)
	introHTML = scrapy.Field()
