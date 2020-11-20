#!/usr/bin/env python3

#
# This script will walk through all the tweet id files and
# hydrate them with twarc. The line oriented JSON files will
# be placed right next to each tweet id file.

from pathlib import Path
from twarc import Twarc
from pyspark import SparkConf, SparkContext
import sys
from os import listdir

twarc = Twarc(consumer_key="ledLMTpVEnaY8Dk4qXH980RfM", consumer_secret="Mza5q9YYJpVpIULpIdQILi3V5ftlrBB158Ec2KIK8rI0B0kss3",
                 access_token="1219964306911059969-CO8zw9O2w61PFl46Q7jRrgbrqkGLxy", access_token_secret="8ymranCmZ2sOPFcYj9AYPnIWPBRMMVXRaSYVmCRHUedmN")

def extractInfo(tweet):
    hydrated_info = {}
    hydrated_info['id'] = tweet['id_str']
    hydrated_info['favorite_count'] = tweet['favorite_count']
    hydrated_info['retweet_count'] = tweet['retweet_count']
    hydrated_info['geo'] = tweet['geo']
    hydrated_info['create_at'] = tweet['created_at']
    return hydrated_info

def main(input_dir, outpath):
    conf = SparkConf().setMaster("local").setAppName("Test")
    sc = SparkContext(conf=conf)
    json_list = []
    pathcounter = 0
    for file in listdir(input_dir):
        for tweet in twarc.hydrate(Path(input_dir + "/" + file).open()):
            json_list.append(tweet)
            if len(json_list) == 5000:
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

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
