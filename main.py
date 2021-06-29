import subprocess
from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.database import database_settings
import click


@click.group()
def cli():
	pass


@cli.command()
@click.argument('spider')
@click.option('--fail', type=int, default=0, help='time of retrying for failed items. default is 0, when the value is negative, retrying won\'t stop unless the table `request_failed` is empty')
def crawl(spider: str, fail: int):
	'''
	start SPIDER crawling using scrapy

	SPIDER: name of the spider to start
	'''
	command = f'scrapy crawl {spider}'
	subprocess.call(command.split(' '))
	if fail != 0:
		command = f'{command} -a fail=on'
	if fail > 0:
		for _ in range(0, fail): subprocess.call(command.split(' '))
	elif fail < 0:
		db = BangumiDatabase(database_settings.CONFIG)
		type_list = []
		if spider == 'bangumi_anime_api':
			type_list = ['anime_api', 'episode']
		if spider == 'bangumi_anime_list':
			type_list = ['id']
		if spider == 'bangumi_anime_scrape':
			type_list = ['anime_scrape']
		if spider == 'bangumi_book_list':
			type_list = ['id']
		if spider == 'bangumi_game_list':
			type_list = ['id']
		if spider == 'bangumi_music_list':
			type_list = ['id']
		if spider == 'bangumi_real_list':
			type_list = ['id']
		flag = True
		while flag:
			subprocess.call(command.split(' '))
			flag = False
			for type in type_list:
				if db.read_fail_list(type=type) != []:
					flag = True


@cli.command()
def initdb():
	'''
	init bangumi database
	'''
	BangumiDatabase(database_settings.CONFIG)


if __name__ == '__main__':
	cli()
