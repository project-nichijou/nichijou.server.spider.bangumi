import traceback
from bangumi.tools.time import BangumiTimeTool
from bangumi.database import bangumi_database_command as db_commands
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
		cursor.execute(db_commands.CREATE_TABLE_BANGUMI_ID)
		cursor.execute(db_commands.CREATE_TABLE_BANGUMI_ANIME)
		cursor.execute(db_commands.CREATE_TABLE_BANGUMI_ANIME_NAME)
		cursor.execute(db_commands.CREATE_TABLE_BANGUMI_ANIME_EPISODE)
		cursor.execute(db_commands.CREATE_TABLE_LOG)
		cursor.execute(db_commands.CREATE_TABLE_REQUEST_FAILED)
		cursor.close()

	def write(self, table: str, values: dict):
		try:
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
		except Exception as e:
			self.write(table='log', values={
				'time': BangumiTimeTool.get_time_str(),
				'content': (
					'exception caught when writing to database. \n'
					f' table: {table} \n'
					f' values: {repr(values)}'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})
	
	def read_sid_list(self, type: str):
		try:
			cursor = self.database.cursor()

			query = f'SELECT `sid` FROM bangumi_id WHERE `type` = {repr(type)}'
			cursor.execute(query)
			
			res = []
			for sid in cursor:
				res.append(sid[0])
			cursor.close()
			return res
		except Exception as e:
			self.write(table='log', values={
				'time': BangumiTimeTool.get_time_str(),
				'content': (
					'exception caught when reading sid list. \n'
					f' type: {type} \n'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})

	def read_fail_list(self, type: str):
		try:
			cursor = self.database.cursor()

			query = f'SELECT `id` FROM request_failed WHERE `type` = {repr(type)}'
			cursor.execute(query)
			
			res = []
			for id in cursor:
				res.append(id[0])
			cursor.close()
			return res
		except Exception as e:
			self.write(table='log', values={
				'time': BangumiTimeTool.get_time_str(),
				'content': (
					'exception caught when reading fail list. \n'
					f' type: {type} \n'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})
	
	def read_by_sid(self, table: str, sid: int):
		try:
			cursor = self.database.cursor(dictionary=True)

			query = f'SELECT * FROM {table} WHERE `sid` = {sid}'
			cursor.execute(query)
			res = cursor.fetchall()

			cursor.close()
			return res
		except Exception as e:
			self.write(table='log', values={
				'time': BangumiTimeTool.get_time_str(),
				'content': (
					'exception caught when reading item by sid. \n'
					f' table: {table} \n'
					f' sid: {repr(sid)}'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})

	def del_fail(self, type: str, id: int):
		try:
			cursor = self.database.cursor()

			delete = f'DELETE FROM request_failed WHERE `type` = {repr(type)} AND `id` = {repr(id)}'
			cursor.execute(delete)

			self.database.commit()
			cursor.close()
		except Exception as e:
			self.write(table='log', values={
				'time': BangumiTimeTool.get_time_str(),
				'content': (
					'exception caught when deleting failed item [resolved]. \n'
					f' type: {type} \n'
					f' id: {repr(id)}'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})

	def del_log_all(self):
		try:
			cursor = self.database.cursor()

			delete = 'TRUNCATE `log`'
			cursor.execute(delete)
			
			self.database.commit()
			cursor.close()
		except Exception as e:
			self.write(table='log', values={
				'time': BangumiTimeTool.get_time_str(),
				'content': (
					'exception caught when deleting all loggings. \n'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})
	
	def del_log_till(self, time: str):
		try:
			cursor = self.database.cursor()

			delete = f'DELETE FROM `log` WHERE `time` <= {repr(time)}'
			cursor.execute(delete)
			
			self.database.commit()
			cursor.close()
		except Exception as e:
			self.write(table='log', values={
				'time': BangumiTimeTool.get_time_str(),
				'content': (
					'exception caught when deleting loggings before exact time. \n'
					f' time: {time} \n'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})

	def close(self):
		self.database.close()
