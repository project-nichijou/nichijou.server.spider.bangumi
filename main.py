from bangumi.database.bangumi_database import BangumiDatabase

import os
import yaml

root_dir = os.path.split(os.path.abspath(__file__))[0]
config_dir = os.path.join(root_dir, 'config.yml')

def read_conf(conf_dir):
	# Read configuration
	with open(conf_dir, 'r', encoding='utf8') as f:
		contents = f.read()
		return yaml.load(contents, Loader=yaml.FullLoader)

if __name__ == '__main__':
	db = BangumiDatabase(read_conf(config_dir)['database'])
