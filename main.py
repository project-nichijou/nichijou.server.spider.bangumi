from bangumi.database.bangumi_database import BangumiDatabase
from common.cookies.cookies_io import write_cookies
import subprocess
import click
import json


@click.group()
def cli():
	pass


@cli.command()
@click.argument('spider')
@click.option('-f', '--fail', 'fail', type=int, default=0, help='time of retrying for failed items. default is 0, when the value is negative, retrying won\'t stop unless the table `request_failed` is empty. Note: this parameter is not available for all spiders, only for `bangumi_anime_api`, `bangumi_anime_scrape`.')
@click.option('-F', '--only-fail', 'only_fail', type=bool, default=False, help='whether only crawl for the failed cases or crawl the whole target')
def crawl(spider: str, fail: int, only_fail: bool):
	'''
	start SPIDER crawling using scrapy

	SPIDER: name of the spider to start
	'''
	command = f'scrapy crawl {spider}'
	if not only_fail:
		subprocess.call(command.split(' '))
	if fail != 0:
		command = f'{command} -a fail=on'
	if fail > 0:
		for _ in range(0, fail): subprocess.call(command.split(' '))
	elif fail < 0:
		db = BangumiDatabase()
		while len(db.read_fail(spider)) > 0:
			subprocess.call(command.split(' '))


@cli.command()
@click.option('--before', type=str, default=None, help='delete the loggings which are before the time in the database. default is None, which means delete all. data format: YYYY-MM-DD hh:mm:ss')
def dellog(before: str):
	'''
	delete loggings in the database.
	'''
	db = BangumiDatabase()
	db.delete_log(before)


@cli.command()
@click.argument('cookies')
def setcookies(cookies: str):
	'''
	set cookies of bangumi

	COOKIES: dictionary of cookies (converted to str)
	'''
	write_cookies(json.loads(cookies))


@cli.command()
def initdb():
	'''
	init bangumi database
	'''
	BangumiDatabase()


if __name__ == '__main__':
	cli()
