from bangumi import bangumi_settings
from bangumi.items.bangumi_id import BangumiIDItem
import scrapy


class BangumiListSpider(scrapy.Spider):
	name = 'bangumi_list'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]
	start_page = 1

	def __init__(self, **kwargs):
		self.update_properties()
		super().__init__(**kwargs)
	
	def update_properties(self):
		self.page_var = self.start_page
		self.start_urls = [self.get_current_url()]

	def get_current_url(self):
		return f'{bangumi_settings.BASE_URL}/{self.type}/browser/?sort=title&page={self.page_var}'

	def parse(self, response):
		# //*[@id="browserItemList"]/li
		item_list = scrapy.Selector(response=response).xpath('//*[@id="browserItemList"]/li')
		# if empty then return
		if len(item_list) == 0:
			return
		# if not empty, yeild results
		for item in item_list:
			result = BangumiIDItem()
			result['id'] = item.attrib['id'][5:] # get rid of the prefix `item_`
			result['type'] = self.type
			result['cn_name'] = item.xpath('./div/h3/a/text()').get()
			result['name'] = item.xpath('./div/h3/small[@class="grey"]/text()').get()
			if result['name'] == None: result['name'] = result['cn_name']
			yield result
		self.page_var += 1
		yield scrapy.Request(self.get_current_url())
