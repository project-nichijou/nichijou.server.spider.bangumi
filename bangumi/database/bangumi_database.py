from common.database.database import CommonDatabase
from bangumi.database import bangumi_database_command as db_commands
import traceback
import mysql.connector
import copy

from mysql.connector import cursor

class BangumiDatabase(CommonDatabase):
	
	def __init__(self, database=None, config=None):
		# use parent's init
		super().__init__(database=database, config=config)
		# create new table
		self.execute(db_commands.CREATE_TABLE_BANGUMI_ID)


	def read_sid(self, type: str):
		'''
		return `sid` list of specific `type`
		'''
		vals = self.read_all('bangumi_id', ['sid'], {
			'type': type
		})
		res = []
		for item in vals:
			res.append(item['sid'])
		return res
