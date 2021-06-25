#!/bin/bash

### get current directory
CURRENT_DIR=$(pwd)

### get the directory of script
SOURCE="$0"
# resolve $SOURCE until the file is no longer a symlink
while [ -h "$SOURCE"  ]; do
    DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"
    SOURCE="$(readlink "$SOURCE")"
	# if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    [[ $SOURCE != /*  ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"

### change to script's directory
cd $DIR

### run spiders
scrapy crawl bangumi_anime_list
scrapy crawl bangumi_anime
scrapy crawl bangumi_anime_episode
scrapy crawl bangumi_anime_episode_intro -a full=on

### go back to the original directory
cd $CURRENT_DIR
