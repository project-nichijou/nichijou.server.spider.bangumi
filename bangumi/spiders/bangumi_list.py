from bangumi import bangumi_settings
import scrapy


class BangumiListSpider(scrapy.Spider):
	name = 'bangumi_list'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]
	start_page = 1

	def __init__(self, **kwargs):
		self.update_properties()
		super().__init__(**kwargs)
	
	def update_properties(self):
		self.start_urls = [f'{bangumi_settings.BASE_URL}/{self.type}/browser/?sort=title&page={self.start_page}']
		self.page_var = self.start_page

	def parse(self, response):
		pass

