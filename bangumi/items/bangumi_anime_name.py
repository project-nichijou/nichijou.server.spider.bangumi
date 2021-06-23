import scrapy

# 无论什么名字：别名、中文、日文
class BangumiAnimeNameItem(scrapy.Item):
	# anime sid
	sid = scrapy.Field()
	# name
	name = scrapy.Field()
