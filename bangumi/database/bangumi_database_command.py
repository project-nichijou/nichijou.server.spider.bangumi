
CREATE_TABLE_BANGUMI_ID = (
	'CREATE TABLE IF NOT EXISTS `bangumi_id` ('
	'	`sid`		INT UNSIGNED NOT NULL,'
	'	`type`		VARCHAR(10) NOT NULL,'
	'	`name`		VARCHAR(200) NOT NULL,'
	'	`name_cn`	VARCHAR(200) NOT NULL,'
	'	PRIMARY KEY ( `sid` ),'
	'	UNIQUE KEY ( `sid` )'
	') ENGINE=InnoDB CHARSET=utf8mb4'
)

CREATE_TABLE_BANGUMI_ANIME = (
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
	') ENGINE=InnoDB CHARSET=utf8mb4'
)

CREATE_TABLE_BANGUMI_ANIME_NAME = (
	'CREATE TABLE IF NOT EXISTS `bangumi_anime_name` ('
	'	`sid`		INT UNSIGNED NOT NULL,'
	'	`name`		VARCHAR(200) NOT NULL,'
	'	PRIMARY KEY ( `sid`, `name` )'
	') ENGINE=InnoDB CHARSET=utf8mb4'
)

CREATE_TABLE_BANGUMI_ANIME_EPISODE = (
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
	') ENGINE=InnoDB CHARSET=utf8mb4'
)

CREATE_TABLE_REQUEST_FAILED = (
	'CREATE TABLE IF NOT EXISTS `request_failed` ('
	'	`id`		INT UNSIGNED NOT NULL,'
	'	`type`		VARCHAR(20) NOT NULL,'
	'	`desc`		LONGTEXT,'
	'	PRIMARY KEY ( `id`, `type` )'
	') ENGINE=InnoDB CHARSET=utf8mb4'
)

CREATE_TABLE_LOG = (
	'CREATE TABLE IF NOT EXISTS `log` ('
	'	`time`		VARCHAR(20) NOT NULL,'
	'	`content`	LONGTEXT'
	') ENGINE=InnoDB CHARSET=utf8mb4'
)
