from pyspark import SparkConf, SparkContext
import ast

def getHeat(jsondata):
    dic = ast.literal_eval(jsondata)
    res1 = dic["text"]
    res2 = dic["favorite_count"]
    res3 = dic["retweet"]
    result = []
    heat = res2 + res3
    if heat == 0:
        for word in res1.split(" "):
            result.append((word.rstrip("\n"), 1))
    else:
        for word in res1.split(" "):
            result.append((word.rstrip("\n"), heat))
    return result

def main():
    conf = SparkConf().setMaster("local").setAppName("Test")
    sc = SparkContext(conf=conf)
    data_26 = sc.textFile("/user/ja3802/26/*/*")
    counts = data_26.map(lambda json: getHeat(json)).\
        flatMap(lambda x:x).\
        reduceByKey(lambda x, y: x + y).\
        map(lambda kv: (kv[1],kv[0])).\
        sortByKey(False).take(10)

    print(counts)

if __name__ == "__main__":
    main()