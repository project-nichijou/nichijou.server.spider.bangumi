#!/bin/bash

START_TIME=`date +%s`

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

### go back to the original directory
cd $CURRENT_DIR

### calculate time
END_TIME=`date +%s`
EXECUTING_TIME=`expr $END_TIME - $START_TIME`

echo "time consumed: "$EXECUTING_TIME" seconds"
