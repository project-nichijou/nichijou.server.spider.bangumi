# 0x00 Bangumi Spider [Project Nichijou]

本项目作为项目[Project Nichijou](https://github.com/project-nichijou)中的子项目，是[Bangumi 番组计划](bgm.tv)的爬虫，用于构建番剧数据库。完整内容详见: https://github.com/project-nichijou/intro

## 思路与流程

本repo只包含：
- 数据爬取
- 写入数据库

如果阅读代码可以发现，我们对于大量难以处理的字段使用了直接写入`HTML`的方式，会在后续的流程中 (见[项目架构](https://github.com/project-nichijou/intro)) 进行处理。这样做的原因在于：

1. 提高爬虫速度 (毕竟服务器是小水管 1C2G)
2. 降低在爬取阶段的报错、解析失败、写入失败频率
3. 有利于提高整体工作的稳定性，方便调试
4. 降低数据库复杂度，方便维护

## 关于数据库

本项目目前使用MySQL作为数据库，更多的数据库日后~~可能~~会进行支持，如果有兴趣可以提交PR，持续关注。

此外，当前的默认数据库名称为`bangumi`，本工具会自动新建数据库以及数据表 (若不存在) 。如果和本地数据库名称有冲突，可以在`bangumi/database/database_settings.py`中修改。

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
