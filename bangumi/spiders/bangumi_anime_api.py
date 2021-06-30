from bangumi.tools import bangumi_cookies
from bangumi.items.bangumi_anime_episode import BangumiAnimeEpisodeItem
from bangumi.items.bangumi_anime_name import BangumiAnimeNameItem
from bangumi.items.bangumi_anime_fail import BangumiAnimeFailItem
from bangumi.items.bangumi_anime import BangumiAnimeAPIItem
from bangumi.config import bangumi_settings
from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.database import database_settings
import scrapy
import traceback
import json


class BangumiAnimeAPISpider(scrapy.Spider):
	name = 'bangumi_anime_api'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]

	def __init__(self, fail='off', *args, **kwargs):
		super(BangumiAnimeAPISpider, self).__init__(*args, **kwargs)
		database = BangumiDatabase(database_settings.CONFIG)
		sid_list = []
		if fail == 'on': sid_list = database.read_fail_list('anime_api')
		else: sid_list = database.read_sid_list('anime')
		self.start_values = [
			{'url': f'{bangumi_settings.BASE_API_URL}/subject/{sid}?responseGroup=large', 'sid': sid} for sid in sid_list
		]
	
	def request(self, url, callback, errback, cb_kwargs=None):
		'''
		warpper for scrapy.request
		'''
		request = scrapy.Request(url=url, callback=callback, errback=errback, cb_kwargs=cb_kwargs, meta={'cookiejar': 'bangumi'})
		headers = bangumi_settings.HEADERS
		for key in headers.keys():
			request.headers[key] = headers[key]
		return request

	def start_requests(self):
		for _, val in enumerate(self.start_values):
			yield self.request(url=val['url'], callback=self.parse, errback=self.errback, cb_kwargs={'sid': val['sid']})

	def parse(self, response, sid):
		# define anime item
		result = BangumiAnimeAPIItem()

		### JUDGE FAILING SECTION
		# sid
		result['sid'] = sid
		# fail
		fail_res = BangumiAnimeFailItem(id=result['sid'], type='anime_api')
		# api request
		api_res = {}
		try:
			api_res = json.loads(response.text)
		except:
			fail_res['desc'] = 'api response format error, cannot convert to json'
			yield fail_res
			return
		# if None then quit
		if api_res == {} or api_res == None:
			fail_res['desc'] = 'api response empty'
			yield fail_res
			return
		
		### API SECTION
		try:
			# name section
			result['name'] = api_res.get('name')
			result['name_cn'] = api_res.get('name_cn')
			yield BangumiAnimeNameItem(sid=result['sid'], name=result['name'])
			if result['name_cn'] != None and result['name_cn'] != '':
				yield BangumiAnimeNameItem(sid=result['sid'], name=result['name_cn'])
			else: result['name_cn'] = result['name']
			
			result['summary'] = api_res.get('summary')
			result['eps_count'] = api_res.get('eps_count')
			result['date'] = api_res.get('air_date')
			result['weekday'] = api_res.get('air_weekday')
			if api_res.get('images') == None: result['image'] = None
			else:
				if 'large' in api_res['images'].keys(): result['image'] = api_res['images']['large']
				elif 'common' in api_res['images'].keys(): result['image'] = api_res['images']['common']
				elif 'medium' in api_res['images'].keys(): result['image'] = api_res['images']['medium']
				elif 'small' in api_res['images'].keys(): result['image'] = api_res['images']['small']
				elif 'grid' in api_res['images'].keys(): result['image'] = api_res['images']['grid']
			if api_res.get('rating') == None: result['rating'] = None
			else: result['rating'] = api_res.get('rating').get('score')
			result['rank'] = api_res.get('rank')
			yield result
		except Exception as e:
			fail_res['desc'] = (
				'exception caught when handling API fields. \n'
				f' exception info: {repr(e)} \n'
				f' traceback: \n'
				f' {traceback.format_exc()}'
			)
			yield fail_res
			return
		
		### API Episode section
		eps = api_res.get('eps')
		if eps == None: return
		for ep in eps:
			try:
				ep_res = BangumiAnimeEpisodeItem()
				ep_res['sid'] = result['sid']
				ep_res['eid'] = ep['id']
				ep_res['type'] = ep['type']
				ep_res['sort'] = ep['sort']
				ep_res['status'] = ep['status']
				ep_res['duration'] = ep['duration']
				ep_res['date'] = ep['airdate']
				ep_res['desc'] = ep['desc']
				ep_res['name'] = ep['name']
				ep_res['name_cn'] = ep['name_cn']
				if ep_res['name_cn'] == None or ep_res['name_cn'] == '':
					ep_res['name_cn'] = ep_res['name']
				yield ep_res
			except Exception as e:
				fail_res['desc'] = (
					'exception caught when handling episodes in API. \n'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
				yield fail_res

	def errback(self, failure):
		sid = failure.request.cb_kwargs['sid']
		yield BangumiAnimeFailItem(id=sid, type='anime_api', desc=(
			'exception caught in errback: \n'
			f' {repr(failure)} \n'
			f' traceback: \n'
			f' {failure.getTraceback()}'
		))
