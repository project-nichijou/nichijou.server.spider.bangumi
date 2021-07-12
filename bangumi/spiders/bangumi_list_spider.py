from common.utils.logger import format_log
from common.utils.datetime import get_time_str_now
from common.items.log_item import CommonLogItem
from bangumi.items.bangumi_id import BangumiIDItem
from bangumi.config import bangumi_settings
from common.spiders.common_spider import CommonSpider
from common.config import settings as common_settings

import re
import requests
import scrapy
import traceback


class BangumiListSpider(CommonSpider):
	
	# scrapy
	name = 'bangumi_list'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]

	# common
	use_cookies = False
	
	# private
	start_page = 1
	last_page = None
	page_count = {}
	sid_list = []


	def __init__(self, **kwargs):
		'''
		initializer for spider
		'''
		self.page_var = self.start_page
		self.get_last_page()
		if self.last_page:
			self.start_values = [
				{'url': self.get_url(page=pg), 'page': pg} for pg in range(1, self.last_page + 1)
			]
		else: self.start_values = [{'url': self.get_url(), 'page': self.page_var}]
		super().__init__(**kwargs)


	def get_last_page(self):
		'''
		get the number of last page to confirm scrape range
		'''
		cur_url = self.get_url()
		first_page_html = requests.get(cur_url, headers=common_settings.HEADERS).content.decode('utf-8')
		self.last_page = int(re.findall('page=[0-9][0-9]*', first_page_html)[-1][5:])
		print("last_page:", self.last_page)


	def get_url(self, page=None, type=None):
		'''
		generate url used for scraping
		'''
		type = self.type if not type else type
		page = self.page_var if not page else page
		return f'{bangumi_settings.BASE_URL}/{type}/browser/?sort=title&page={page}'


	def start_requests(self):
		'''
		scraping entrance
		'''
		for _, val in enumerate(self.start_values):
			yield self.request(url=val['url'], callback=self.parse, errback=self.errback, cb_kwargs={'page': val['page']})


	def parse(self, response, page):
		# Update cookies
		# cookies = response.headers.getlist('Set-Cookie')
		# bangumi_cookies.update_cookies(cookies)
		
		# //*[@id="browserItemList"]/li
		item_list = scrapy.Selector(response=response).xpath('//*[@id="browserItemList"]/li')
		# if empty then return
		if len(item_list) == 0:
			return
		
		self.page_count[str(page)] = 0
		
		# if not empty, yeild results
		for item in item_list:
			result = BangumiIDItem()
			try:
				result['sid'] = int(item.attrib['id'][5:])	# get rid of the prefix `item_`
				result['type'] = self.type
				result['name_cn'] = item.xpath('./div/h3/a/text()').get()
				result['name'] = item.xpath('./div/h3/small[@class="grey"]/text()').get()
				if result['name'] == None: result['name'] = result['name_cn']
				
				### logging section
				self.page_count[str(page)] += 1
				
				if result['sid'] in self.sid_list:
					log_dict = dict(result)
					log_dict['page'] = page
					yield CommonLogItem(
						time = get_time_str_now(),
						content = format_log(
							info = 'duplicate `sid` detected! (in `bangumi_list`)',
							values = log_dict
						)
					)
				else: self.sid_list.append(result['sid'])
				
				yield result
			except Exception as e:
				log_dict = dict(result)
				log_dict['page'] = page
				yield CommonLogItem(
					time = get_time_str_now(),
					content = format_log(
						info = 'exception caught in `bangumi_list`',
						exception = e,
						traceback = traceback.format_exc(),
						values = log_dict
					)
				)
		
		if self.page_count[str(page)] < 24:
			yield CommonLogItem(
				time = get_time_str_now(),
				content = format_log(
					info = 'list count warning! (in bangumi_list)',
					values = {
						'page': page,
						'type': self.type,
						'count': self.page_count[str(page)],
						'last_page': self.last_page,
						'url': self.get_url(page=page)
					}
				)
			)

		if page == self.last_page:
			self.last_page = None
			self.page_var = page

		if not self.last_page:
			self.page_var += 1
			yield self.request(url=self.get_url(), callback=self.parse, errback=self.errback, cb_kwargs={'page': self.page_var})
