from bangumi.database.bangumi_database import BangumiDatabase
from common.pipelines.storing_pipeline import CommonStoringPipeline


class BangumiStoringPipeline(CommonStoringPipeline):

	def __init__(self):
		self.database = BangumiDatabase()
