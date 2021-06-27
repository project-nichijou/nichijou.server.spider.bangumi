import scrapy


class BangumiAnimeItem(scrapy.Item):
	### Bangumi API
	# subject id
	sid = scrapy.Field()
	# 原名
	name = scrapy.Field()
	# 中文名 (没有就是原名)
	name_cn = scrapy.Field()
	# 简介
	summary = scrapy.Field()
	# 话数 (猜测: 只有正片)
	eps_count = scrapy.Field()
	# 放送开始日期
	date = scrapy.Field()
	# 放送星期
	weekday = scrapy.Field()
	# 封面图, large > common > medium > small > grid
	image = scrapy.Field()
	# 评分, rating.score
	rating = scrapy.Field()
	# 站内排名
	rank = scrapy.Field()

	### 私有爬取	
	# 所有属性列表 (HTML)
	metaHTML = scrapy.Field()
	# 标签, 空格隔开
	tags = scrapy.Field()
	# 种类: TV, OVA, ...
	type = scrapy.Field()
