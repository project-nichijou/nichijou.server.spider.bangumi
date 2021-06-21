import scrapy


class BangumiAnimeItem(scrapy.Item):
	# subject id
	sid = scrapy.Field()
	# 原名
	name = scrapy.Field()
	# 中文名 (没有就是原名)
	cn_name = scrapy.Field()
	# 简介
	intro = scrapy.Field()
	# 话数
	episode = scrapy.Field()
	# 放送开始
	start = scrapy.Field()
	# 其他 (HTML)
	moreHTML = scrapy.Field()
