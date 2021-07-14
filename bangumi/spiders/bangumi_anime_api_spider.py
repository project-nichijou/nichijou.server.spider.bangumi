from bangumi.items.bangumi_episode_name_item import BangumiEpisodeNameItem
from bangumi.items.bangumi_episode_item import BangumiEpisodeItem
from bangumi.items.bangumi_anime_name_item import BangumiAnimeNameItem
from common.utils.checker import is_not_null, is_null
import traceback
from common.utils.formatter import format_airing_status, format_date, format_duration, format_episode_type, format_id, format_int, format_log, format_weekday
from common.utils.hash import get_md5
from common.items.fail_request_item import CommonFailedRequestItem
import json
from bangumi.items.bangumi_anime_item import BangumiAnimeAPIItem
from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.config import bangumi_settings
from common.spiders.common_spider import CommonSpider


class BangumiAnimeAPISpider(CommonSpider):

	# scrapy
	name = 'bangumi_anime_api'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]

	# common
	use_cookies = False


	def init_normal_datasource(self):
		sid_list = BangumiDatabase().read_sid('anime')
		self.start_values = [
			{
				'url': f'{bangumi_settings.BASE_API_URL}/subject/{sid}?responseGroup=large',
				'sid': sid
			} for sid in sid_list
		]


	def init_fail_datasource(self):
		failed_items = BangumiDatabase().read_fail(self.name)
		self.start_values = [
			{
				'url': item['url'],
				'sid': int(json.loads(item['params'])['sid'])
			} for item in failed_items
		]


	def start_requests(self):
		for _, val in enumerate(self.start_values):
			yield self.request(url=val['url'], callback=self.parse, errback=self.errback, cb_kwargs={'sid': val['sid']})


	def parse(self, response, sid):
		url = str(response.url)

		result = BangumiAnimeAPIItem()
		result._url = url
		id = format_id(sid)
		
		result['id'] = sid
		result['url'] = url
		
		result_fail = CommonFailedRequestItem(
			url = url,
			url_md5 = get_md5(url),
			spider = self.name,
			params = json.dumps({'sid': sid})
		)

		api_res = {}
		try:
			api_res = json.loads(response.text)
		except Exception as e:
			result_fail['desc'] = format_log(
				info = 'api response format error, cannot convert to json',
				exception = e,
				traceback = traceback.format_exc(),
				values = {
					'url': url,
					'sid': sid 
				}
			)
			yield result_fail
			return
		
		if is_null(api_res):
			result_fail['desc'] = format_log(
				info = 'api response empty',
				values = {
					'url': url,
					'sid': sid 
				}
			)
			yield result_fail
			return
		
		try:
			result['name'] = api_res.get('name')
			result['name_cn'] = api_res.get('name_cn')
			if is_not_null(result['name']):
				yield BangumiAnimeNameItem(
					id = id,
					name = result['name']
				)
			else: result['name'] = result['name_cn']
			if is_not_null(result['name_cn']):
				yield BangumiAnimeNameItem(
					id = id,
					name = result['name']
				)

			identifier = {
				'sid': sid,
				'spider': self.name,
				'url': url
			}

			result['desc'] = api_res.get('summary')
			result['eps_cnt'] = format_int(api_res.get('eps_count'), identifier)
			result['date'] = format_date(api_res.get('air_date'), identifier)
			result['weekday'] = format_weekday(api_res.get('air_weekday'), identifier)

			if api_res.get('images') == None: result['image'] = None
			else:
				if 'large' in api_res['images'].keys(): result['image'] = api_res['images']['large']
				elif 'common' in api_res['images'].keys(): result['image'] = api_res['images']['common']
				elif 'medium' in api_res['images'].keys(): result['image'] = api_res['images']['medium']
				elif 'small' in api_res['images'].keys(): result['image'] = api_res['images']['small']
				elif 'grid' in api_res['images'].keys(): result['image'] = api_res['images']['grid']
			
			if is_null(api_res.get('rating')): result['rating'] = None
			else: result['rating'] = api_res.get('rating').get('score')

			result['rank'] = api_res.get('rank')

			yield result
		except Exception as e:
			result_fail['desc'] = format_log(
				info = 'exception caught when handling API fields',
				exception = e,
				traceback = traceback.format_exc(),
				values = {
					'api_res': api_res,
					'item': result
				}
			)
			yield result_fail
			return
		
		eps = api_res.get('eps')
		if is_null(eps): return

		for ep in eps:
			result_ep = BangumiEpisodeItem()
			try:
				identifier['ep'] = ep.get('id')

				result_ep['id'] = id
				result_ep['type'] = format_episode_type(ep.get('type'), identifier)
				result_ep['sort'] = ep.get('sort')
				result_ep['url'] = f'https://bgm.tv/ep/{ep.get("id")}'
				result_ep['name'] = ep.get('name')
				result_ep['name_cn'] = ep.get('name_cn')
				result_ep['status'] = format_airing_status(ep.get('status'), identifier)
				result_ep['duration'] = format_duration(ep.get('duration'), identifier)
				result_ep['date'] = format_date(ep.get('airdate'), identifier)
				result_ep['desc'] = ep.get('desc')
				yield result_ep

				if is_not_null(result_ep['name']):
					yield BangumiEpisodeNameItem(
						id = id,
						type = result_ep['type'],
						sort = result_ep['sort'],
						name = result_ep['name']
					)
				if is_not_null(result_ep['name_cn']):
					yield BangumiEpisodeNameItem(
						id = id,
						type = result_ep['type'],
						sort = result_ep['sort'],
						name = result_ep['name_cn']
					)
			except Exception as e:
				result_fail['desc'] = format_log(
					info = 'exception caught when handling episodes in API.',
					exception = e,
					traceback = traceback.format_exc(),
					values = {
						'api_res': api_res,
						'ep_item': result_ep
					}
				)
				yield result_fail
				return
