import mysql.connector
import copy

class BangumiDatabase(object):
	
	def __init__(self, config):
		self.config = config
		self.check_database()
		self.database = mysql.connector.connect(**config)
		self.check_tables()

	def check_database(self):
		t_config = copy.deepcopy(self.config)
		if 'database' in t_config.keys():
			t_config.pop('database')
		db = mysql.connector.connect(**t_config)
		cursor = db.cursor()
		cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{self.config["database"]}`')
		cursor.close()

	def check_tables(self):
		cursor = self.database.cursor()
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS `bangumi_id` ('
			'	`sid`		INT UNSIGNED NOT NULL,'
			'	`type`		VARCHAR(10) NOT NULL,'
			'	`name`		VARCHAR(200) NOT NULL,'
			'	`cn_name`	VARCHAR(200) NOT NULL,'
			'	PRIMARY KEY ( `sid` )'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS `bangumi_anime` ('
			'	`sid`		INT UNSIGNED NOT NULL,'
			'	`name`		VARCHAR(200) NOT NULL,'
			'	`cn_name`	VARCHAR(200) NOT NULL,'
			'	`introHTML`	LONGTEXT,'
			'	`episode`	INT,'
			'	`start`		VARCHAR(100),'
			'	`moreHTML`	LONGTEXT,'
			'	PRIMARY KEY ( `sid` )'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS `bangumi_anime_episode` ('
			'	`eid`		INT UNSIGNED NOT NULL,'
			'	`sid`		INT UNSIGNED NOT NULL,'
			'	`name`		VARCHAR(200) NOT NULL,'
			'	`cn_name`	VARCHAR(200) NOT NULL,'
			'	`type`		VARCHAR(10) NOT NULL,'
			'	`count`		INT UNSIGNED NOT NULL,'
			'	`order`		INT UNSIGNED NOT NULL,'
			'	`introHTML`	LONGTEXT,'
			'	PRIMARY KEY ( `eid` )'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.close()

	def close(self):
		self.database.close()
