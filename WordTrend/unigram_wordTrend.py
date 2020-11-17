from pyspark import SparkConf, SparkContext
import ast
import re

#The list of stop words is provided by nltk
stop_words = []
for sw in open("stopwords_en"):
    stop_words.append(sw.rstrip("\n"))
stop_words = set(stop_words)

#calculate trending and preprocess text
def getHeat(jsondata):
    dic = ast.literal_eval(jsondata)
    text = dic["text"]
    res2 = dic["favorite_count"]
    res3 = dic["retweet"]
    result = []
    heat = (res2 + res3)//10

    #remove URLS, remove mentions, for hashtags only keep the text
    text = re.sub("(https:\/\/\S+)|(@\S+)|([,.#?!()-])", "", text)
    #remove new line characters
    text_noNewline = re.sub("(\n)", " ", text)

    for word in text_noNewline.split(" "):
        if word and word.lower() not in stop_words:
            result.append((word.lower(), 1 + heat))

    return result

def main():
    conf = SparkConf().setMaster("local").setAppName("Test")
    sc = SparkContext(conf=conf)
    data_26 = sc.textFile("/user/ja3802/26/*/*")
    counts = data_26.map(lambda json: getHeat(json)).\
        flatMap(lambda x:x).\
        reduceByKey(lambda x, y: x + y).\
        map(lambda kv: (kv[1],kv[0])).\
        sortByKey(False).take(30)

    print(counts)

if __name__ == "__main__":
    main()