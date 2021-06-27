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
	# 类型: 本篇 0 / SP 1 / OP 2 / ED 3 / 预告,宣传,广告 4 / MAD 5 / 其他 6
	type = scrapy.Field()
	# 顺序 (当前type中的多少话)
	sort = scrapy.Field()
	# 是否已放送 状态: Air / NA / Today
	status = scrapy.Field()
	# 时常, e.g. 24m
	duration = scrapy.Field()
	# 放送日期
	airdate = scrapy.Field()
	# 简介
	desc = scrapy.Field()
