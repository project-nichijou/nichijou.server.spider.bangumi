from bangumi.items.bangumi_anime_episode import BangumiAnimeEpisodeItem
from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.database import database_settings
from bangumi import bangumi_settings
import scrapy


class BangumiAnimeEpisodeSpider(scrapy.Spider):
	name = 'bangumi_anime_episode'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]

	def __init__(self, fail='off', *args, **kwargs):
		super(BangumiAnimeEpisodeSpider, self).__init__(*args, **kwargs)
		database = BangumiDatabase(database_settings.CONFIG)
		sid_list = []
		if fail == 'on': sid_list = database.read_fail_list('episode')
		else: sid_list = database.read_sid_list('anime')
		self.start_urls = [
			f'{bangumi_settings.BASE_URL}/subject/{sid}/ep' for sid in sid_list
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
		# sid
		sid = int(str(response.url).split('/')[-2])
		# episode list
		e_list = scrapy.Selector(response=response).xpath('//*[@id="columnInSubjectA"]/form/div/ul/li')
		e_type = '本篇'
		e_order = 0
		for episode in e_list:
			e_class = episode.xpath('./@class').get()
			if e_class == 'cat':
				e_type = episode.xpath('./text()').get()
			elif str(e_class).endswith('clearit'): pass
			else:
				e_order += 1
				e_status = episode.xpath('./h6/span[@class="epAirStatus"]/span/@class').get()
				e_name = episode.xpath('./h6/a/text()').get()
				eid = int(str(episode.xpath('./h6/a/@href').get()).split('/')[-1])
				e_name_cn = episode.xpath('./h6/span[@class="tip"]/text()').get()
				if e_name_cn == None or e_name_cn == '':
					e_name_cn = e_name
				else:
					if str(e_name_cn).startswith(' / '):
						e_name_cn = e_name_cn[3:]
					type = e_type
					if type == '本篇': type = ''
					e_name_cn = f'{type}{e_order}.{e_name_cn}'
				yield BangumiAnimeEpisodeItem(
					eid = eid,
					sid = sid,
					name = e_name,
					name_cn = e_name_cn,
					type = e_type,
					order = e_order,
					status = e_status
				)
