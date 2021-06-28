from bangumi.tools.time import BangumiTimeTool
import scrapy


class BangumiLogItem(scrapy.Item):
	# time: %Y-%m-%d %H:%M:%S
	time = scrapy.Field()
	# content
	content = scrapy.Field()

	@staticmethod
	def create(content):
		return BangumiLogItem(time=BangumiTimeTool.get_time_str(), content=content)
