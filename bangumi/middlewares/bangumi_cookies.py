from bangumi.spiders.bangumi_anime_scrape import BangumiAnimeScrapeSpider
from bangumi.config import bangumi_settings
from scrapy.http.cookies import CookieJar
from bangumi.tools import bangumi_cookies
from bangumi import settings
from scrapy.http import Response
from scrapy.utils.python import to_unicode
from scrapy import signals
import logging
import requests


logger = logging.getLogger(__name__)

class BangumiCookiesMiddleware:
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the downloader middleware does not modify the
	# passed objects.

	jar = CookieJar()

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_request(self, request, spider):
		# Called for each request that goes through the downloader
		# middleware.
		if request.meta.get('dont_merge_cookies', False):
			return
		# judge type of spider
		if not isinstance(spider, BangumiAnimeScrapeSpider):
			return
		cookies_dict = requests.utils.dict_from_cookiejar(self.jar)
		if cookies_dict == {} or cookies_dict == None:
			for cookie in self._get_request_cookies(self.jar, request):
				self.jar.set_cookie_if_ok(cookie, request)

		# set Cookie header
		request.headers.pop('Cookie', None)
		self.jar.add_cookie_header(request)
		self._debug_cookie(request, spider)
		# for cookie in self.jar:
		# 	print(bangumi_cookies.cookie_to_dict(cookie))
		# Must either:
		# - return None: continue processing this request
		# - or return a Response object
		# - or return a Request object
		# - or raise IgnoreRequest: process_exception() methods of
		#   installed downloader middleware will be called
		return None

	def process_response(self, request, response, spider):
		# Called with the response returned from the downloader.
		if request.meta.get('dont_merge_cookies', False):
			return response
		# judge type of spider
		if not isinstance(spider, BangumiAnimeScrapeSpider):
			return response
		# extract cookies from Set-Cookie and drop invalid/expired cookies
		self.jar.extract_cookies(response, request)
		self._debug_set_cookie(response, spider)
		# Write cookies
		if bangumi_settings.COOKIES_AUTO_UPDATE:
			cookies = []
			for cookie in self.jar:
				cookies.append(bangumi_cookies.cookie_to_dict(cookie))
			bangumi_cookies.write_cookies(cookies)
		# Must either;
		# - return a Response object
		# - return a Request object
		# - or raise IgnoreRequest
		return response

	def process_exception(self, request, exception, spider):
		# Called when a download handler or a process_request()
		# (from other downloader middleware) raises an exception.

		# Must either:
		# - return None: continue processing this exception
		# - return a Response object: stops process_exception() chain
		# - return a Request object: stops process_exception() chain
		pass

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)

	def _debug_cookie(self, request, spider):
		if settings.COOKIES_DEBUG:
			cl = [to_unicode(c, errors='replace')
				  for c in request.headers.getlist('Cookie')]
			if cl:
				cookies = "\n".join(f"Cookie: {c}\n" for c in cl)
				msg = f"Sending cookies to: {request}\n{cookies}"
				logger.debug(msg, extra={'spider': spider})

	def _debug_set_cookie(self, response, spider):
		if settings.COOKIES_DEBUG:
			cl = [to_unicode(c, errors='replace')
				  for c in response.headers.getlist('Set-Cookie')]
			if cl:
				cookies = "\n".join(f"Set-Cookie: {c}\n" for c in cl)
				msg = f"Received cookies from: {response}\n{cookies}"
				logger.debug(msg, extra={'spider': spider})

	def _format_cookie(self, cookie, request):
		"""
		Given a dict consisting of cookie components, return its string representation.
		Decode from bytes if necessary.
		"""
		decoded = {}
		for key in ("name", "value", "path", "domain"):
			if cookie.get(key) is None:
				if key in ("name", "value"):
					msg = "Invalid cookie found in request {}: {} ('{}' is missing)"
					logger.warning(msg.format(request, cookie, key))
					return
				continue
			if isinstance(cookie[key], str):
				decoded[key] = cookie[key]
			else:
				try:
					decoded[key] = cookie[key].decode("utf8")
				except UnicodeDecodeError:
					logger.warning("Non UTF-8 encoded cookie found in request %s: %s",
								   request, cookie)
					decoded[key] = cookie[key].decode("latin1", errors="replace")

		cookie_str = f"{decoded.pop('name')}={decoded.pop('value')}"
		for key, value in decoded.items():  # path, domain
			cookie_str += f"; {key.capitalize()}={value}"
		return cookie_str
	
	def _get_request_cookies(self, jar, request):
		"""
		Extract cookies from the Request.cookies attribute
		"""
		if not request.cookies:
			return []
		elif isinstance(request.cookies, dict):
			cookies = ({"name": k, "value": v} for k, v in request.cookies.items())
		else:
			cookies = request.cookies
		formatted = filter(None, (self._format_cookie(c, request) for c in cookies))
		response = Response(request.url, headers={"Set-Cookie": formatted})
		return jar.make_cookies(response, request)
