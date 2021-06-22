# 0x00 Bangumi Spider [Project Nichijou]

本项目作为项目`Project Nichijou`中的子项目，是[Bangumi 番组计划](bgm.tv)的爬虫，用于构建番剧数据库。

## 环境

- MySQL 5.7.4 +
- Python 3.6 +
- Scrapy
- Ubuntu (WSL)

## 配置方法

本项目有两个配置文件：
- `bangumi/bangumi_settings.py`
- `bangumi/database/database_settings.py`

可以发现这两个文件在本`repo`中只有`_template`，需要将这两个`template`配置好并复制、重命名。

关于配置字段的具体含义，文件中都有注释，可以自行查阅。

注意：`bangumi_settings`中的`COOKIES`在某些情况下需要以下字段，~~否则无法爬取特殊内容~~:

```
{
	"chii_auth": <value>
}
```

## 使用方法

现阶段还没有做专门的启动器、服务器，可以直接通过以下命令启动爬虫：

```
scrapy crawl <spider_name>
```

`<spider_name>`即为蜘蛛的文件名，位于`bangumi/spider/`目录下。

注意：对于部分蜘蛛，如`bangumi_anime`，有额外的参数。如果需要传参，请使用如下命令：

```
scarpy crawl <spider_name> -a <arg1>=<val1> <arg2>=<val2> ...
```

比如：

```
scrapy crawl bangumi_anime -a fail=off
```
