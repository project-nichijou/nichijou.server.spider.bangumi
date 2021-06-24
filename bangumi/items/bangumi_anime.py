import scrapy


class BangumiAnimeItem(scrapy.Item):
	# subject id
	sid = scrapy.Field()
	# 原名
	name = scrapy.Field()
	# 中文名 (没有就是原名)
	cn_name = scrapy.Field()
	# 简介 (HTML)
	introHTML = scrapy.Field()
	# 话数
	episode = scrapy.Field()
	# 放送开始
	start = scrapy.Field()
	# 所有属性列表 (HTML)
	attrHTML = scrapy.Field()
	# 标签, 空格隔开
	tags = scrapy.Field()
	# 种类: TV, OVA, ...
	type = scrapy.Field()
	# 缩略图
	thumb = scrapy.Field()
