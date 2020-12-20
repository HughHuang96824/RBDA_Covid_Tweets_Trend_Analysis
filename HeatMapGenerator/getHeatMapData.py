import sys

import parseTime as pt
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark import sql
import ast


#calculate trending and preprocess text
def getTime(list_of_info):
    tp = list_of_info[0]
    score = list_of_info[1]
    create_at = tp[0]
    geo = tp[1]
    like = tp[2]
    rt = tp[3]
    time = pt.parse(create_at)
    return (time, geo, like, rt, score)

def toKV(line):
    dic = ast.literal_eval(line)
    id = dic['id']
    return (id, [dic['create_at'], dic['geo'], dic['favorite_count'], dic['retweet_count']])

def main(tweet_path, dataset_path):
    conf = SparkConf().setMaster("local").setAppName("Test")
    sc = SparkContext(conf=conf)

    sqlContext = sql.SQLContext(sc)

    # join
    #senti_score = sc.textFile("/user/ja3802/geo-data/*").map(lambda line: (line.split(",")[0], float(line.split(",")[1])))
    senti_score = sc.textFile(dataset_path).map(lambda line: line.split(","))\
        .filter(lambda line: len(line) == 2).map(lambda line: (line[0], float(line[1])))

    #$senti_score.saveAsTextFile("err")
    geodata = sc.textFile(tweet_path).map(lambda line: toKV(line))
    fulldata = geodata.join(senti_score)
    #fulldata.saveAsTextFile("fulldata")

    timeKey = fulldata.map(lambda json: getTime(json[1]))
    time_df = timeKey.toDF(["time","geo", "like", "rt", "score"])
    time_df.write.partitionBy("time").json("heatmapdata")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])