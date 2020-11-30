import sys
from pathlib import Path

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark import sql
from os import listdir

def main(input_dir, result_path):
    conf = SparkConf().setMaster("yarn-client").setAppName("avg").set('spark.executor.memory', '4G').set('spark.driver.memory', '4G').set('spark.driver.maxResultSize', '4G')
    sc = SparkContext(conf=conf)

    sqlContext = sql.SQLContext(sc)
    with open(result_path, "a") as f:

        for file in listdir(input_dir):
            sum = None
            count = None
            with open(input_dir + "/" + file) as in_f:
                lines = in_f.read().splitlines()
                rdd = sc.parallelize(lines)
                row_rdd = rdd.map(lambda line: line.split(",")).filter(lambda line: len(line) == 2)
                sum = row_rdd.map(lambda line: (float(line[1]))).sum()
                count = row_rdd.count()
                in_f.close()

                f.write(file + " " + str(sum) + " " + str(count) + " " + str(sum / count) +"\n")

        f.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

