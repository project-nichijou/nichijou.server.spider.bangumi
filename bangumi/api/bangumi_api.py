from bangumi.config import bangumi_settings
import requests


class BangumiAPI():
	
	@staticmethod
	def get_subject(sid: int):
		try:
			return requests.get(f'{bangumi_settings.BASE_API_URL}/subject/{sid}?responseGroup=large', headers=bangumi_settings.HEADERS, cookies=bangumi_settings.COOKIES).json()
		except:
			return {}
