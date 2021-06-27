import scrapy


class BangumiAnimeEpisodeItem(scrapy.Item):
	# episode id
	eid = scrapy.Field()
	# subject id
	sid = scrapy.Field()
	# 原名
	name = scrapy.Field()
	# 中文名 (没有就是原名)
	name_cn = scrapy.Field()
	# 类型: 本篇 / SP / OP / ED / etc.
	type = scrapy.Field()
	# 顺序 (所有剧集中的第几话, 从1开始)
	order = scrapy.Field()
	# 是否已放送 状态: Air / NA
	status = scrapy.Field()
