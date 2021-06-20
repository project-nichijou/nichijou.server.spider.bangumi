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
# Protocol of spider, type: SpiderProtocol
SPIDER_PROTOCOL = SpiderProtocol.HTTPS

# URL of original site
ORIGIN_DOMAIN = 'bgm.tv'
# URL of mirror site
MIRROR_DOMAIN = 'mirror.bgm.rincat.ch'

# Define Base URL
if SPIDER_MODE == SpiderMode.ORIGIN:
	BASE_DOMAIN = ORIGIN_DOMAIN
	BASE_URL = f'{SPIDER_PROTOCOL.value}{ORIGIN_DOMAIN}'
if SPIDER_MODE == SpiderMode.MIRROR:
	BASE_DOMAIN = MIRROR_DOMAIN
	BASE_URL = f'{SPIDER_PROTOCOL.value}{MIRROR_DOMAIN}'
