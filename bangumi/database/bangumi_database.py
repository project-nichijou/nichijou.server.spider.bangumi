import mysql.connector
import copy

from mysql.connector import cursor

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
			'	`name_cn`	VARCHAR(200) NOT NULL,'
			'	PRIMARY KEY ( `sid` ),'
			'	UNIQUE KEY ( `sid` )'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS `bangumi_anime` ('
			'	`sid`		INT UNSIGNED NOT NULL,'
			'	`name`		VARCHAR(200) NOT NULL,'
			'	`name_cn`	VARCHAR(200) NOT NULL,'
			'	`summary`	LONGTEXT,'
			'	`eps_count`	INT,'
			'	`date`		VARCHAR(200),'
			'	`weekday`	INT,'
			'	`metaHTML`	LONGTEXT,'
			'	`tags`		LONGTEXT,'
			'	`type`		VARCHAR(10),'
			'	`image`		LONGTEXT,'
			'	`rating`	DECIMAL(32,28),'
			'	`rank`		INT,'
			'	PRIMARY KEY ( `sid` ),'
			'	UNIQUE KEY ( `sid` )'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS `bangumi_anime_name` ('
			'	`sid`		INT UNSIGNED NOT NULL,'
			'	`name`		VARCHAR(200) NOT NULL,'
			'	PRIMARY KEY ( `sid`, `name` )'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS `bangumi_anime_episode` ('
			'	`eid`		INT UNSIGNED NOT NULL,'
			'	`sid`		INT UNSIGNED NOT NULL,'
			'	`name`		VARCHAR(200) NOT NULL,'
			'	`name_cn`	VARCHAR(200) NOT NULL,'
			'	`type`		INT UNSIGNED NOT NULL,'
			'	`sort`		INT UNSIGNED NOT NULL,'
			'	`status`	VARCHAR(10) NOT NULL,'
			'	`duration`	VARCHAR(200) NOT NULL,'
			'	`date`		VARCHAR(200) NOT NULL,'
			'	`desc`		LONGTEXT,'
			'	PRIMARY KEY ( `eid` ),'
			'	UNIQUE KEY ( `eid` )'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS `request_failed` ('
			'	`id`		INT UNSIGNED NOT NULL,'
			'	`type`		VARCHAR(20) NOT NULL,'
			'	`desc`		LONGTEXT,'
			'	PRIMARY KEY ( `id`, `type` )'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS `log` ('
			'	`time`		VARCHAR(20) NOT NULL,'
			'	`content`	LONGTEXT'
			') ENGINE=InnoDB CHARSET=utf8'
		)
		cursor.close()

	def write(self, table: str, values: dict):
		keys = values.keys()
		
		cmd_line_table = f'INSERT INTO {table} '
		cmd_line_keys = f'({", ".join(f"`{key}`" for key in keys)}) '
		cmd_line_values = f'VALUES ({", ".join(f"%({key})s" for key in keys)}) '
		cmd_line_update = f'ON DUPLICATE KEY UPDATE {", ".join(f"`{key}` = %({key})s" for key in keys)}'
		
		command = '\n'.join([cmd_line_table, cmd_line_keys, cmd_line_values, cmd_line_update])

		cursor = self.database.cursor()
		cursor.execute(command, values)

		self.database.commit()
		cursor.close()
	
	def read_sid_list(self, type: str):
		cursor = self.database.cursor()

		query = f'SELECT `sid` FROM bangumi_id WHERE `type` = {repr(type)}'
		cursor.execute(query)
		
		res = []
		for sid in cursor:
			res.append(sid[0])
		cursor.close()
		return res

	def read_fail_list(self, type: str):
		cursor = self.database.cursor()

		query = f'SELECT `id` FROM request_failed WHERE `type` = {repr(type)}'
		cursor.execute(query)
		
		res = []
		for id in cursor:
			res.append(id[0])
		cursor.close()
		return res
	
	def read_by_sid(self, table: str, sid: int):
		cursor = self.database.cursor(dictionary=True)

		query = f'SELECT * FROM {table} WHERE `sid` = {sid}'
		cursor.execute(query)
		res = cursor.fetchall()

		cursor.close()
		return res

	def del_fail(self, type: str, id: int):
		cursor = self.database.cursor()

		delete = f'DELETE FROM request_failed WHERE `type` = {repr(type)} AND `id` = {repr(id)}'
		cursor.execute(delete)

		self.database.commit()
		cursor.close()

	def del_log_all(self):
		cursor = self.database.cursor()

		delete = 'TRUNCATE `log`'
		cursor.execute(delete)
		
		self.database.commit()
		cursor.close()
	
	def del_log_till(self, time: str):
		cursor = self.database.cursor()

		delete = f'DELETE FROM `log` WHERE `time` <= {repr(time)}'
		cursor.execute(delete)
		
		self.database.commit()
		cursor.close()

	def close(self):
		self.database.close()
