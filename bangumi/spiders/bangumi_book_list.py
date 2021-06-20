import scrapy
from bangumi.spiders.bangumi_list import BangumiListSpider


class BangumiBookListSpider(BangumiListSpider):
	name = 'bangumi_book_list'
	type = 'book'
	start_page = 1

