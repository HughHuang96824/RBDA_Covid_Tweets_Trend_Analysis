#!/usr/bin/env python3

#
# This script will walk through all the tweet id files and
# hydrate them with twarc. The line oriented JSON files will
# be placed right next to each tweet id file.

import json
from pathlib import Path
from twarc import Twarc
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

import sys

twarc = Twarc(consumer_key="ledLMTpVEnaY8Dk4qXH980RfM", consumer_secret="Mza5q9YYJpVpIULpIdQILi3V5ftlrBB158Ec2KIK8rI0B0kss3",
                 access_token="1219964306911059969-CO8zw9O2w61PFl46Q7jRrgbrqkGLxy", access_token_secret="8ymranCmZ2sOPFcYj9AYPnIWPBRMMVXRaSYVmCRHUedmN")


def main(input_path):
    conf = SparkConf().setMaster("local").setAppName("download tweet")
    sc = SparkContext(conf=conf)

    json_list = []

    for tweet in twarc.hydrate(Path(input_path).open()):
        # print(type(tweet)) returns <class 'dict'>
        json_list.append(json.dumps(tweet).encode('utf8'))# + b"\n"

    rdd = sc.parallelize(json_list)#.map(lambda x: json.dumps(x))
    sql_ctx = SQLContext(sc)
    df = sql_ctx.read.json(rdd)
    df.write.format('json').save("/user/ja3802/d1/test_out")


if __name__ == "__main__":
    #name of input file
    main(sys.argv[1])