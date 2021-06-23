from bangumi.items.bangumi_anime_name import BangumiAnimeNameItem
from bangumi.items.bangumi_anime_fail import BangumiAnimeFailItem
from bangumi.items.bangumi_anime import BangumiAnimeItem
from bangumi import bangumi_settings
from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.database import database_settings
import scrapy
import time


class BangumiAnimeSpider(scrapy.Spider):
	name = 'bangumi_anime'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]

	def __init__(self, fail='on', *args, **kwargs):
		super(BangumiAnimeSpider, self).__init__(*args, **kwargs)
		database = BangumiDatabase(database_settings.CONFIG)
		sid_list = []
		if fail == 'on': sid_list = database.read_fail_list('anime')
		else: sid_list = database.read_sid_list('anime')
		self.start_urls = [
			f'{bangumi_settings.BASE_URL}/subject/{sid}' for sid in sid_list
		]
	
	def request(self, url, callback):
		'''
		warpper for scrapy.request
		'''
		request = scrapy.Request(url=url, callback=callback)
		cookies = bangumi_settings.COOKIES
		for key in cookies.keys():
			request.cookies[key] = cookies[key]
		headers = bangumi_settings.HEADERS
		for key in headers.keys():
			request.headers[key] = headers[key]
		return request

	def start_requests(self):
		for i, url in enumerate(self.start_urls):
			yield self.request(url, self.parse)

	def parse(self, response):
		result = BangumiAnimeItem()
		# sid
		result['sid'] = int(str(response.url).split('/')[-1])
		# info HTML <ul id="infobox">
		result['attrHTML'] = scrapy.Selector(response=response).xpath('//*[@id="infobox"]').get()
		# name
		result['name'] = scrapy.Selector(response=response).xpath('//*[@id="headerSubject"]/h1/a/text()').get()
		# if None then quit
		if result['name'] == None:
			fail_res = BangumiAnimeFailItem()
			fail_res['id'] = result['sid']
			fail_res['type'] = 'anime'
			return fail_res
		# set default cn_name
		result['cn_name'] = result['name']
		yield BangumiAnimeNameItem(
			sid = result['sid'],
			name = result['name']
		)
		# introHTML
		result['introHTML'] = scrapy.Selector(response=response).xpath('//*[@id="subject_summary"]').get()
		# default episode
		result['episode'] = 0
		# detailed info
		for item in scrapy.Selector(response=response).xpath('//*[@id="infobox"]/li'):
			# [:-2] 去掉末尾的 `: `
			info_title = item.xpath('./span/text()').extract()[0][:-2]
			try: raw = item.xpath('./text()').get()
			except: continue
			if raw == None or raw == '': continue
			# cn_name
			if info_title == '中文名':
				result['cn_name'] = raw
				yield BangumiAnimeNameItem(
					sid = result['sid'],
					name = result['cn_name']
				)
			# 别名
			if info_title == '别名':
				yield BangumiAnimeNameItem(
					sid = result['sid'],
					name = raw
				)
			# episode
			if info_title == '话数':
				try: result['episode'] = int(raw)
				except: pass
			# start date
			if info_title in bangumi_settings.START_INFO:
				try:
					tArray = time.strptime(raw, "%Y年%m月%d日")
					date = time.strftime('%Y-%m-%d', tArray)
					result['start'] = date
				except:
					try:
						tArray = time.strptime(raw, "%Y-%m-%d")
						date = time.strftime('%Y-%m-%d', tArray)
						result['start'] = date
					except:
						result['start'] = None
		yield result

def get_field_value(selector, index=0):
    return selector[index] if len(selector) != 0 else ''
