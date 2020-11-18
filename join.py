from pyspark import SparkContext
import ast

def toKV(line):
    dic = ast.literal_eval(line)
    id = dic['id']
    del dic['text']
    del dic['id']
    return (id, [dic['favorite_count'], dic['retweet']])

if __name__ == "__main__":
    sc=SparkContext("local", "join")
    
    df1 = sc.textFile("26/*/*").map(lambda line: toKV(line))
    df2 = sc.textFile("corona_tweets_26.csv").map(lambda line: line.split(",")).map(lambda line: (line[0], float(line[1])))
    df1.join(df2).saveAsTextFile('delete')
   

    
