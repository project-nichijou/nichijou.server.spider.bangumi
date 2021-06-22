from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.database import database_settings

if __name__ == '__main__':
	db = BangumiDatabase(database_settings.CONFIG)
	db.write('bangumi_id', {
		'sid': 296367,
		'type': 'anime',
		'name': 'SSSS.DYNAZENON',
		'cn_name': 'SSSS.电光机王'
	})
