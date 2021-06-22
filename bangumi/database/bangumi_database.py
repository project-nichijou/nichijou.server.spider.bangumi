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
			'	PRIMARY KEY ( `sid` ),'
			'	UNIQUE KEY ( `sid` )'
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
			'	`attrHTML`	LONGTEXT,'
			'	PRIMARY KEY ( `sid` ),'
			'	UNIQUE KEY ( `sid` )'
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
			'	PRIMARY KEY ( `eid` ),'
			'	UNIQUE KEY ( `eid` )'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.close()

	def write(self, table: str, values: dict):
		keys = values.keys()
		
		cmd_line_table = f'INSERT INTO {table} '
		cmd_line_keys = f'({", ".join(key for key in keys)}) '
		cmd_line_values = f'VALUES ({", ".join(f"%({key})s" for key in keys)}) '
		cmd_line_update = f'ON DUPLICATE KEY UPDATE {", ".join(f"{key} = %({key})s" for key in keys)}'
		
		command = '\n'.join([cmd_line_table, cmd_line_keys, cmd_line_values, cmd_line_update])

		cursor = self.database.cursor()
		cursor.execute(command, values)

		self.database.commit()
		cursor.close()

	def close(self):
		self.database.close()
