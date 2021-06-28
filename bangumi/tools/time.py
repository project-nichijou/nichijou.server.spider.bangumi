import time

class BangumiTimeTool():

	@staticmethod
	def get_time_str():
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
