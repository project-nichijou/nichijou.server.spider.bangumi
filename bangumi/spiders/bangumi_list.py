from bangumi.config import bangumi_settings
from bangumi.items.bangumi_id import BangumiIDItem
import scrapy
import re
import requests


class BangumiListSpider(scrapy.Spider):
	name = 'bangumi_list'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]
	start_page = 1
	last_page = None

	def __init__(self, **kwargs):
		self.update_properties()
		super().__init__(**kwargs)
	
	def get_last_page(self):
		cur_url = self.get_current_url()
		first_page_html = requests.get(cur_url,headers=bangumi_settings.HEADERS).content.decode('utf-8')
		self.last_page=int(re.findall('page=[0-9][0-9]*',first_page_html)[-1][5:])
		print("last_page:",self.last_page)
	
	def update_properties(self):
		self.page_var = self.start_page
		self.get_last_page()
		if self.last_page:
			self.start_urls = [self.get_url_from_params(_page=pg) for pg in range(1,self.last_page+1)]
		else: self.start_urls=[self.get_current_url()]

	def get_url_from_params(self,_page=None,_type=None):
		_type = self.type if not _type else _type
		_page = self.page_var if not _page else _page
		return f'{bangumi_settings.BASE_URL}/{_type}/browser/?sort=title&page={_page}'

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
			result['sid'] = item.attrib['id'][5:] # get rid of the prefix `item_`
			result['type'] = self.type
			result['name_cn'] = item.xpath('./div/h3/a/text()').get()
			result['name'] = item.xpath('./div/h3/small[@class="grey"]/text()').get()
			if result['name'] == None: result['name'] = result['name_cn']
			yield result

		if not self.last_page:
			self.page_var += 1
			yield scrapy.Request(self.get_current_url())
