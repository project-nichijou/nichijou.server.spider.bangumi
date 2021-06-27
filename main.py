from bangumi.database.bangumi_database import BangumiDatabase
from bangumi.database import database_settings
from scrapy import cmdline
import click


@click.group()
def cli():
	pass


@cli.command()
@click.argument('spider')
@click.option('--fail', is_flag=True, default=False, help='whether start in fail mode')
def crawl(spider: str, fail: bool):
	'''
	start SPIDER crawling using scrapy

	SPIDER: name of the spider to start
	'''
	command = f'scrapy crawl {spider}'
	if fail:
		command = f'{command} -a'
	if fail:
		command = f'{command} fail=on'
	cmdline.execute(command.split(' '))


@cli.command()
def initdb():
	'''
	init bangumi database
	'''
	BangumiDatabase(database_settings.CONFIG)


if __name__ == '__main__':
	cli()
