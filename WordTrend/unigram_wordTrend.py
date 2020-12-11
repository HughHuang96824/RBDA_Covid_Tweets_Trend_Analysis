import sys

from pyspark import SparkConf, SparkContext
import ast
import re

#The list of stop words is provided by nltk
stop_words = []
for sw in open("../../../temp_git/WordTrend/stopwords_en"):
    stop_words.append(sw.rstrip("\n"))
stop_words = set(stop_words)

#calculate trending and preprocess text
def getHeat(jsondata):
    dic = ast.literal_eval(jsondata)
    text = dic["text"]
    res2 = dic["favorite_count"]
    res3 = dic["retweet"]
    result = []
    interations = res2 + res3

    #remove URLS, remove mentions, for hashtags only keep the text
    text = re.sub("(https:\/\/\S+)|(@\S+)|([,.#?!()\-])", "", text)
    #remove new line characters
    text_noNewline = re.sub("(\n)", " ", text)

    for word in text_noNewline.split(" "):
        if word and word.lower() not in stop_words:
            result.append((word.lower(), 1 + interations))

    return result

def main(outpath, topk):
    conf = SparkConf().setMaster("local").setAppName("Test")
    sc = SparkContext(conf=conf)
    for i in range(1,59):

        data_i = sc.textFile("/user/ja3802/"+str(i)+"/*/*")
        counts = data_i.map(lambda json: getHeat(json)).\
            flatMap(lambda x:x).\
            reduceByKey(lambda x, y: x + y).\
            map(lambda kv: (kv[1],kv[0])).\
            sortByKey(False).take(topk)
        result_path = outpath + "/" + str(i)
        with open(result_path, "a") as f:
            f.write("\n".join(str(item) for item in counts))
            f.close()
        print(counts)

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))