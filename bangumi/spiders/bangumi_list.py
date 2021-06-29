from bangumi.items.bangumi_log import BangumiLogItem
from bangumi.config import bangumi_settings
from bangumi.items.bangumi_id import BangumiIDItem
import scrapy
import re
import requests
import traceback


class BangumiListSpider(scrapy.Spider):
	name = 'bangumi_list'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]
	start_page = 1
	last_page = None
	page_count = {}
	sid_list = []

	def __init__(self, **kwargs):
		self.page_var = self.start_page
		self.get_last_page()
		if self.last_page:
			self.start_values = [
				{'url': self.get_url(page=pg), 'page': pg} for pg in range(1, self.last_page + 1)
			]
		else: self.start_values = [{'url': self.get_url(), 'page': self.page_var}]
		super().__init__(**kwargs)
	
	def get_last_page(self):
		cur_url = self.get_url()
		first_page_html = requests.get(cur_url, headers=bangumi_settings.HEADERS, cookies=bangumi_settings.COOKIES).content.decode('utf-8')
		self.last_page = int(re.findall('page=[0-9][0-9]*', first_page_html)[-1][5:])
		print("last_page:", self.last_page)

	def request(self, url, callback, errback, cb_kwargs=None):
		'''
		warpper for scrapy.request
		'''
		request = scrapy.Request(url=url, callback=callback, errback=errback, cb_kwargs=cb_kwargs)
		cookies = bangumi_settings.COOKIES
		for key in cookies.keys():
			request.cookies[key] = cookies[key]
		headers = bangumi_settings.HEADERS
		for key in headers.keys():
			request.headers[key] = headers[key]
		return request
	
	def start_requests(self):
		for _, val in enumerate(self.start_values):
			yield self.request(url=val['url'], callback=self.parse, errback=self.errback, cb_kwargs={'page': val['page']})

	def get_url(self, page=None, type=None):
		type = self.type if not type else type
		page = self.page_var if not page else page
		return f'{bangumi_settings.BASE_URL}/{type}/browser/?sort=title&page={page}'

	def parse(self, response, page):
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
					yield BangumiLogItem.create(content=(
						'duplicate sid detected! (in bangumi_list) \n'
						f' type: {self.type} \n'
						f' page: {page} \n'
						f' sid: {result["sid"]} \n'
						f' name: {result["name"]} \n'
						f' name_cn: {result["name_cn"]}'
					))
				else: self.sid_list.append(result['sid'])
				###
				yield result
			except Exception as e:
				log_res = BangumiLogItem.create(content=(
					f'exception caught in bangumi_list \n'
					f' type: {self.type} \n'
					f' page: {page} \n'
					f' sid: {result["sid"]} \n'
					f'exception info: {repr(e)} \n'
					f'traceback: \n'
					f'{traceback.format_exc()}'
				))
				yield log_res
		
		if self.page_count[str(page)] < 24:
			yield BangumiLogItem.create(content=(
				'list count warning! (in bangumi_list) \n'
				f' page: {page} \n'
				f' type: {self.type} \n'
				f' count: {self.page_count[str(page)]} \n'
				f' last_page: {self.last_page} \n'
				f' url: {self.get_url(page=page)}'
			))

		if page == self.last_page:
			self.last_page = None
			self.page_var = page

		if not self.last_page:
			self.page_var += 1
			yield self.request(url=self.get_url(), callback=self.parse, errback=self.errback, cb_kwargs={'page': self.page_var})

	def errback(self, failure):
		page = failure.request.cb_kwargs['page']
		yield BangumiLogItem.create(content=(
			f'exception caught in errback of bangumi_list: \n'
			f'{repr(failure)} \n'
			f'traceback: \n'
			f'{failure.getTraceback()} \n'
			f'page: {page}'
		))
