from bangumi.items.bangumi_anime_episode_intro import BangumiAnimeEpisodeIntroItem
from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.database import database_settings
from bangumi import bangumi_settings
import scrapy


class BangumiAnimeEpisodeIntroSpider(scrapy.Spider):
	name = 'bangumi_anime_episode_intro'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]

	def __init__(self, fail='off', *args, **kwargs):
		super(BangumiAnimeEpisodeIntroSpider, self).__init__(*args, **kwargs)
		database = BangumiDatabase(database_settings.CONFIG)
		eid_list = []
		if fail == 'on': eid_list = database.read_fail_list('episode_intro')
		else: eid_list = database.read_eid_list()
		self.start_urls = [
			f'{bangumi_settings.BASE_URL}/ep/{eid}' for eid in eid_list
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
		# eid
		eid = int(str(response.url).split('/')[-1])
		# introHTML
		intro = scrapy.Selector(response=response).xpath('//*[@id="columnEpA"]/div[@class="epDesc"]').get()
		yield BangumiAnimeEpisodeIntroItem(
			eid = eid,
			introHTML = intro
		)
