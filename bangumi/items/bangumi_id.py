import scrapy


class BangumiIDItem(scrapy.Item):
	# subject id
	sid = scrapy.Field()
	# type of subject
	type = scrapy.Field()
	# 原名
	name = scrapy.Field()
	# 中文名 (没有就是原名)
	cn_name = scrapy.Field()
