from bangumi.api.bangumi_api import BangumiAPI
from bangumi.items.bangumi_anime_name import BangumiAnimeNameItem
from bangumi.items.bangumi_anime_fail import BangumiAnimeFailItem
from bangumi.items.bangumi_anime import BangumiAnimeItem
from bangumi import bangumi_settings
from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.database import database_settings
import scrapy
import traceback


class BangumiAnimeSpider(scrapy.Spider):
	name = 'bangumi_anime'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]

	def __init__(self, fail='off', *args, **kwargs):
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
		# define anime item
		result = BangumiAnimeItem()

		### JUDGE FAILING SECTION
		# sid
		result['sid'] = int(str(response.url).split('/')[-1])
		# fail
		fail_res = BangumiAnimeFailItem(id=result['sid'], type='anime')
		# api request
		api_res = BangumiAPI.get_subject(result['sid'])
		# name
		name = scrapy.Selector(response=response).xpath('//*[@id="headerSubject"]/h1/a/text()').get()
		# if None then quit
		if name == None or name == '':
			fail_res['desc'] = f'name from web page is none. may be 404, please check cookies. \n original response: {response.text}'
			return fail_res
		if api_res == {} or api_res == None:
			fail_res['desc'] = 'api response empty'
			return fail_res
		
		### API SECTION
		try:
			# name section
			result['name'] = api_res['name']
			result['name_cn'] = api_res['name_cn']
			yield BangumiAnimeNameItem(sid=result['sid'], name=result['name'])
			if result['name_cn'] != None and result['name_cn'] != '':
				yield BangumiAnimeNameItem(sid=result['sid'], name=result['name_cn'])
			else: result['name_cn'] = result['name']
			
			result['summary'] = api_res['summary']
			result['eps_count'] = api_res['eps_count']
			result['date'] = api_res['air_date']
			result['weekday'] = api_res['air_weekday']
			if api_res['images'] == None: result['image'] = None
			else:
				if 'large' in api_res['images'].keys(): result['image'] = api_res['images']['large']
				elif 'common' in api_res['images'].keys(): result['image'] = api_res['images']['common']
				elif 'medium' in api_res['images'].keys(): result['image'] = api_res['images']['medium']
				elif 'small' in api_res['images'].keys(): result['image'] = api_res['images']['small']
				elif 'grid' in api_res['images'].keys(): result['image'] = api_res['images']['grid']
			if api_res['rating'] == None: result['rating'] = None
			else: result['rating'] = api_res['rating']['score']
			result['rank'] = api_res['rank']
		except Exception as e:
			fail_res['desc'] = (
				'exception caught when handling API fields. \n'
				f'exception info: {repr(e)} \n'
				f'traceback: \n'
				f'{traceback.format_exc()}'
			)
			return fail_res

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
				f'exception info: {repr(e)} \n'
				f'traceback: \n'
				f'{traceback.format_exc()}'
			)
			yield fail_res
		
		### API Episode section
		# try:
			
		# except Exception as e:
		# 	fail_res['desc'] = (
		# 		'exception caught when handling episodes in API. \n'
		# 		f'exception info: {repr(e)} \n'
		# 		f'traceback: \n'
		# 		f'{traceback.format_exc()}'
		# 	)
		# 	return fail_res

def get_field_value(selector, index=0):
    return selector[index] if len(selector) != 0 else ''
