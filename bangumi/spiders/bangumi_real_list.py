import scrapy
from bangumi.spiders.bangumi_list import BangumiListSpider


class BangumiRealListSpider(BangumiListSpider):
	name = 'bangumi_real_list'
	type = 'real'
	start_page = 1

