
CREATE_TABLE_BANGUMI_ID = (
	'CREATE TABLE IF NOT EXISTS `bangumi_id` ('
	'	`sid`		INT UNSIGNED NOT NULL,'
	'	`type`		VARCHAR(10) NOT NULL,'
	'	`name`		VARCHAR(200) NOT NULL,'
	'	`name_cn`	VARCHAR(200),'
	'	PRIMARY KEY ( `sid` )'
	') ENGINE=InnoDB CHARSET=utf8mb4'
)
