import scrapy


class BangumiAnimeFailItem(scrapy.Item):
	# whatever id
	id = scrapy.Field()
	# type of item
	type = scrapy.Field()
	# error description
	desc = scrapy.Field()
