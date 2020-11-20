#!/usr/bin/env python3

#
# This script will walk through all the tweet id files and
# hydrate them with twarc. The line oriented JSON files will
# be placed right next to each tweet id file.

from pathlib import Path
from twarc import Twarc
from pyspark import SparkConf, SparkContext
import sys

twarc = Twarc(consumer_key="xxx", consumer_secret="xxxxxx", app_auth=True)


def extractInfo(tweet):
    hydrated_info = {}
    hydrated_info['id'] = tweet['id_str']
    hydrated_info['text'] = tweet['full_text']
    hydrated_info['favorite_count'] = tweet['favorite_count']
    hydrated_info['retweet'] = tweet['retweet_count']
    return hydrated_info

def main(input_path, outpath):
    conf = SparkConf().setMaster("local").setAppName("Test")
    sc = SparkContext(conf=conf)
    json_list = []
    pathcounter = 0

    # filter 20000 tweets at a time
    for tweet in twarc.hydrate(Path(input_path).open()):
        json_list.append(tweet)
        if len(json_list) == 20000:
            pathcounter += 1
            path = outpath + str(pathcounter)
            rdd = sc.parallelize(json_list).filter(lambda tweet: "retweeted_status" not in tweet).map(
                lambda tweet: extractInfo(tweet)).saveAsTextFile(path)
            json_list = []

    # filter any remaining ones
    if len(json_list) > 0:
        pathcounter += 1
        path = outpath + str(pathcounter)
        rdd = sc.parallelize(json_list).filter(lambda tweet: "retweeted_status" not in tweet).map(
            lambda tweet: extractInfo(tweet)).saveAsTextFile(path)
        json_list = []

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
