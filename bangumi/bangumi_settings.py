from enum import Enum

# Custom Bangumi Settings

# Enum class of spider mode
class SpiderMode(Enum):
	# using original site
	ORIGIN = 1
	# using mirror site
	MIRROR = 2

# Mode of spider, type: SpiderMode 
SPIDER_MODE = SpiderMode.ORIGIN

# URL of original site
ORIGIN_SITE = 'https://bgm.tv/'
# URL of mirror site
MIRROR_SITE = 'https://mirror.bgm.rincat.ch/'

# Define Base URL
if SPIDER_MODE == SpiderMode.ORIGIN:
	BASE_URL = ORIGIN_SITE
if SPIDER_MODE == SpiderMode.MIRROR:
	BASE_URL = MIRROR_SITE
