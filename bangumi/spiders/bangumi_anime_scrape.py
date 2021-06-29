from bangumi.items.bangumi_anime_name import BangumiAnimeNameItem
from bangumi.items.bangumi_anime_fail import BangumiAnimeFailItem
from bangumi.items.bangumi_anime import BangumiAnimeScrapeItem
from bangumi.config import bangumi_settings
from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.database import database_settings
import scrapy
import traceback


class BangumiAnimeScrapeSpider(scrapy.Spider):
	name = 'bangumi_anime_scrape'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]

	def __init__(self, fail='off', *args, **kwargs):
		super(BangumiAnimeScrapeSpider, self).__init__(*args, **kwargs)
		self.database = BangumiDatabase(database_settings.CONFIG)
		sid_list = []
		if fail == 'on': sid_list = self.database.read_fail_list('anime_scrape')
		else: sid_list = self.database.read_sid_list('anime')
		self.start_values = [
			{'url': f'{bangumi_settings.BASE_URL}/subject/{sid}', 'sid': sid} for sid in sid_list
		]
	
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
			yield self.request(url=val['url'], callback=self.parse, errback=self.errback, cb_kwargs={'sid': val['sid']})

	def parse(self, response, sid):
		# fail
		fail_res = BangumiAnimeFailItem(id=sid, type='anime_scrape')
		api_res = self.database.read_by_sid('bangumi_anime', sid)
		# define anime item
		result = BangumiAnimeScrapeItem(*api_res)
		### JUDGE FAILING SECTION
		# api
		if api_res == None or result == None or api_res == [] or api_res == {} or 'sid' not in dict(result):
			fail_res['desc'] = 'sid not found in database, or fetching value failed. please check the api spider.'
			yield fail_res
			return
		# name
		name = scrapy.Selector(response=response).xpath('//*[@id="headerSubject"]/h1/a/text()').get()
		# if None then quit
		if name == None or name == '':
			fail_res['desc'] = f'name from web page is none. may be 404, please check cookies. \n original response: {response.text}'
			yield fail_res
			return

		### scraping section
		try:
			# meta HTML <ul id="infobox">
			result['metaHTML'] = scrapy.Selector(response=response).xpath('//*[@id="infobox"]').get()
			# detailed info
			for item in scrapy.Selector(response=response).xpath('//*[@id="infobox"]/li'):
				# [:-2] 去掉末尾的 `: `
				info_title = item.xpath('./span/text()').extract()[0][:-2]
				raw = ''
				try: raw = item.xpath('./text()').get()
				except: continue
				if raw == None or raw == '': continue
				if info_title == '别名':
					yield BangumiAnimeNameItem(sid=result['sid'], name=raw)
				# episode
				if info_title == '话数' and (result['eps_count'] == 0 or result['eps_count'] == None):
					try: result['eps_count'] = int(raw)
					except: pass
				# start date
				if info_title in bangumi_settings.START_INFO and (result['date'] == '' or result['date'] == None):
					result['date'] = raw
			# tags
			result['tags'] = ' '.join(scrapy.Selector(response=response).xpath('//*[@id="subject_detail"]/div[@class="subject_tag_section"]/div[1]/a/span/text()').getall())
			if result['tags'] == '无': result['tags'] = None
			# type
			result['type'] = scrapy.Selector(response=response).xpath('//*[@id="headerSubject"]/h1/small/text()').get()
			if result['image'] == '' or result['image'] == None:
				result['image'] = scrapy.Selector(response=response).xpath('//*[@id="bangumiInfo"]/div/div[1]/a/img/@src').get()
			if str(result['image']).startswith('//'):
				result['image'] = f'https:{result["image"]}'
			yield result
		except Exception as e:
			fail_res['desc'] = (
				'exception caught when handling scrapy response. \n'
				f' exception info: {repr(e)} \n'
				f' traceback: \n'
				f' {traceback.format_exc()}'
			)
			yield fail_res

	def errback(self, failure):
		sid = failure.request.cb_kwargs['sid']
		yield BangumiAnimeFailItem(id=sid, type='anime_scrape', desc=(
			'exception caught in errback: \n'
			f' {repr(failure)} \n'
			f' traceback: \n'
			f' {failure.getTraceback()}'
		))
