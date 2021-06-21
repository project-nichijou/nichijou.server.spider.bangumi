import mysql.connector
import copy

class BangumiDatabase(object):
	
	def __init__(self, config):
		self.config = config
		if not self.check_existence():
			self.creat_database()
		self.database = mysql.connector.connect(**config)
		# TODO: check & create `tables`

	def check_existence(self):
		t_config = copy.deepcopy(self.config)
		if 'database' in t_config.keys():
			t_config.pop('database')
		db = mysql.connector.connect(**t_config)
		cursor = db.cursor()
		cursor.execute('SHOW DATABASES')
		for item in cursor:
			if item[0] == self.config['database']:
				return True
		return False
	
	def creat_database(self):
		t_config = copy.deepcopy(self.config)
		if 'database' in t_config.keys():
			t_config.pop('database')
		db = mysql.connector.connect(**t_config)
		cursor = db.cursor()
		cursor.execute(f'CREATE DATABASE {self.config["database"]}')
