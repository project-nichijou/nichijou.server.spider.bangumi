import scrapy


class BangumiIDItem(scrapy.Item):
	id = scrapy.Field()
	type = scrapy.Field()
	name = scrapy.Field()
	cn_name = scrapy.Field()
