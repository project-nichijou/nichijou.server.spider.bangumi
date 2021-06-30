from enum import Enum

# Custom Bangumi Settings

# Enum class of spider mode
class SpiderMode(Enum):
	# using original site
	ORIGIN = 1
	# using mirror site
	MIRROR = 2

# Enum class of spider connecting protocol
class SpiderProtocol(Enum):
	# using http protocal
	HTTP = 'http://'
	# using https protocal
	HTTPS = 'https://'

# Mode of spider, type: SpiderMode 
SPIDER_MODE = SpiderMode.ORIGIN
# Mode of spider for API, type: SpiderMode
API_SPIDER_MODE = SpiderMode.MIRROR
# Protocol of spider, type: SpiderProtocol
SPIDER_PROTOCOL = SpiderProtocol.HTTPS

# DOMAIN of original site
ORIGIN_DOMAIN = 'bgm.tv'
# DOMAIN of mirror site
MIRROR_DOMAIN = 'mirror.bgm.rincat.ch'
# URL of original site
ORIGIN_URL = f'{SPIDER_PROTOCOL.value}{ORIGIN_DOMAIN}'

# API DOMAIN of original site
ORIGIN_API_DOMAIN = 'api.bgm.tv'
# API DOMAIN of mirror site
MIRROR_API_DOMAIN = 'mirror.api.bgm.rincat.ch'

# Define Base URL
if SPIDER_MODE == SpiderMode.ORIGIN:
	BASE_DOMAIN = ORIGIN_DOMAIN
	BASE_URL = f'{SPIDER_PROTOCOL.value}{ORIGIN_DOMAIN}'
if SPIDER_MODE == SpiderMode.MIRROR:
	BASE_DOMAIN = MIRROR_DOMAIN
	BASE_URL = f'{SPIDER_PROTOCOL.value}{MIRROR_DOMAIN}'

if API_SPIDER_MODE == SpiderMode.ORIGIN:
	BASE_API_URL = f'{SPIDER_PROTOCOL.value}{ORIGIN_API_DOMAIN}'
if API_SPIDER_MODE == SpiderMode.MIRROR:
	BASE_API_URL = f'{SPIDER_PROTOCOL.value}{MIRROR_API_DOMAIN}'

HEADERS = {
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
	'sec-ch-ua-mobile': '?0',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Sec-Fetch-Site': 'none',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-User': '?1',
	'Sec-Fetch-Dest': 'document',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}

# whether update the cookies automatically from Cookie-Set
COOKIES_AUTO_UPDATE = True

START_INFO = ['放送开始', '上映年度', '开始']
