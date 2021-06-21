import scrapy


class BangumiAnimeEpisodeItem(scrapy.Item):
	# episode id
	eid = scrapy.Field()
	# subject id
	sid = scrapy.Field()
	# 原名
	name = scrapy.Field()
	# 中文名 (没有就是原名)
	cn_name = scrapy.Field()
	# 类型: 本篇 / SP / OP / ED / etc.
	type = scrapy.Field()
	# 第几话
	count = scrapy.Field()
	# 顺序 (所有剧集中的第几话)
	order = scrapy.Field()
