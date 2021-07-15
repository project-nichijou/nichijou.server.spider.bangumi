from bangumi.items.bangumi_anime_name_item import BangumiAnimeNameItem
from common.utils.ac import ACAutomaton
import traceback

from bs4 import BeautifulSoup
from common.utils.checker import is_not_null, is_null
import scrapy
from common.utils.hash import get_md5
from common.items.fail_request_item import CommonFailedRequestItem
from common.utils.formatter import format_date, format_id, format_int
from common.utils.logger import format_log
from bangumi.items.bangumi_anime_item import BangumiAnimeScrapeItem
import json
from bangumi.database.bangumi_database import BangumiDatabase
from common.spiders.common_spider import CommonSpider
from bangumi.config import bangumi_settings


class BangumiAnimeScrapeSpider(CommonSpider):

	# scrapy
	name = 'bangumi_anime_scrape'
	allowed_domains = [bangumi_settings.BASE_DOMAIN]

	# common
	use_cookies = True


	def init_normal_datasource(self):
		sid_list = BangumiDatabase().read_sid('anime')
		self.start_values = [
			{
				'url': f'{bangumi_settings.BASE_URL}/subject/{sid}',
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

		result = BangumiAnimeScrapeItem()
		result._url = url
		id = format_id(sid)

		result['id'] = id
		result['url'] = url

		result_fail = CommonFailedRequestItem(
			url = url,
			url_md5 = get_md5(url),
			spider = self.name,
			params = json.dumps({'sid': sid})
		)

		name = scrapy.Selector(response=response).xpath('//*[@id="headerSubject"]/h1/a/text()').get()

		if is_null(name):
			result_fail['desc'] = format_log(
				info = 'name from web page is none. may be 404, please check cookies.',
				values = {
					'original-response': response.text
				}
			)
			yield result_fail
			return

		result['name'] = name

		try:
			# meta HTML <ul id="infobox">
			# result['metaHTML'] = scrapy.Selector(response=response).xpath('//*[@id="infobox"]').get()
			soup = BeautifulSoup(scrapy.Selector(response=response).xpath('//*[@id="infobox"]').get(), 'lxml')
			meta = []
			for item in soup.findAll('li'):
				meta.append(item.getText())
			result['meta'] = '\n'.join(meta)

			# detailed info
			for item in scrapy.Selector(response=response).xpath('//*[@id="infobox"]/li'):
				# [:-2] 去掉末尾的 `: `
				info_title = item.xpath('./span/text()').extract()[0][:-2]
				
				raw = ''
				try: raw = item.xpath('./text()').get()
				except: continue
				if is_null(raw): continue

				if ACAutomaton(['别名']).match(str(info_title)):
					yield BangumiAnimeNameItem(
						id = id,
						name = raw
					)
				if ACAutomaton(['话数']).match(str(info_title)):
					eps_cnt = format_int(raw)
					if is_not_null(eps_cnt):
						result['eps_cnt'] = eps_cnt
				if ACAutomaton(['放送开始', '上映年度', '开始']).match(str(info_title)):
					date = format_date(raw)
					if is_not_null(date):
						result['date'] = date
			
			result['tags'] = ' '.join(scrapy.Selector(response=response).xpath('//*[@id="subject_detail"]/div[@class="subject_tag_section"]/div[1]/a/span/text()').getall())
			if result['tags'] == '无': result['tags'] = None

			result['type'] = scrapy.Selector(response=response).xpath('//*[@id="headerSubject"]/h1/small/text()').get()

			result['image'] = scrapy.Selector(response=response).xpath('//*[@id="bangumiInfo"]/div/div[1]/a/img/@src').get()

			if str(result['image']).startswith('//'):
				result['image'] = f'https:{result["image"]}'
			yield result
		except Exception as e:
			result_fail['desc'] = format_log(
				info = 'exception caught when handling scraping response',
				exception = e,
				traceback = traceback.format_exc(),
				values = {
					'original-response': response.text
				}
			)
			yield result_fail
			return
