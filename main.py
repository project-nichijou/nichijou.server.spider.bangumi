from scrapy import cmdline
import click


@click.group()
def cli():
	pass


@cli.command()
@click.argument('spider')
@click.option('--fail', is_flag=True, default=False, help='whether start in fail mode')
@click.option('--full', is_flag=True, default=False, help='this option is only for episode introduction, whether crawl the full list. (extremely time consuming)')
def crawl(spider: str, fail: bool, full: bool):
	'''
	start SPIDER crawling using scrapy

	SPIDER: name of the spider to start
	'''
	command = f'scrapy crawl {spider}'
	if fail or full:
		command = f'{command} -a'
	if fail:
		command = f'{command} fail=on'
	if full:
		command = f'{command} full=on'
	cmdline.execute(command.split(' '))


if __name__ == '__main__':
	cli()
