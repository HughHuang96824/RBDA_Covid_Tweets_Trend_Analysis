#!/usr/bin/env python3

#
# This script will walk through all the tweet id files and
# hydrate them with twarc. The line oriented JSON files will
# be placed right next to each tweet id file.

import json
from pathlib import Path
from twarc import Twarc
from pyspark import SparkConf, SparkContext
import sys

twarc = Twarc(consumer_key="ledLMTpVEnaY8Dk4qXH980RfM", consumer_secret="Mza5q9YYJpVpIULpIdQILi3V5ftlrBB158Ec2KIK8rI0B0kss3",
                 access_token="1219964306911059969-CO8zw9O2w61PFl46Q7jRrgbrqkGLxy", access_token_secret="8ymranCmZ2sOPFcYj9AYPnIWPBRMMVXRaSYVmCRHUedmN")

def extractInfo(tweet):
    hydrated_info = {}
    hydrated_info['id'] = tweet['id_str']
    hydrated_info['text'] = tweet['full_text']
    hydrated_info['favorite_count'] = tweet['favorite_count']
    hydrated_info['retweet'] = tweet['retweet_count']
    if 'location' in tweet:
    	hydrated_info['loc'] = tweet['location']
    else: hydrated_info['loc'] = ''
    return hydrated_info

def main(input_path, outpath):
    conf = SparkConf().setMaster("local").setAppName("Test")
    sc = SparkContext(conf=conf)
    json_list = []
    for tweet in twarc.hydrate(Path(input_path).open()):
	json_list.append(tweet)

    rdd = sc.parallelize(json_list).filter(lambda tweet: "retweeted_status" not in tweet).map(lambda tweet: extractInfo(tweet)).saveAsTextFile(outpath)  


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
