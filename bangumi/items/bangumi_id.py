from common.items.common_item import CommonItem
import scrapy


class BangumiIDItem(CommonItem):

	table = 'bangumi_id'

	primary_keys = ['sid']

	use_fail = True

	# subject id
	sid = scrapy.Field()
	# type of subject
	type = scrapy.Field()
	# 原名
	name = scrapy.Field()
	# 中文名 (没有就是原名)
	name_cn = scrapy.Field()
