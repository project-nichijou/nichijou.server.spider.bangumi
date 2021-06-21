# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# TODO: 处理所有的href, 加上 https://bgm.tv

class BangumiPipeline:
	def process_item(self, item, spider):
		return item
