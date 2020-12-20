from pyspark import SparkContext
import numpy as np
import sys, getopt
from pyspark.mllib.stat import Statistics

def parseLine(line):
	k = 0
	s = ""
	for i in line:
		if i == "\"":
			k += 1
		elif i == ",":
			if k % 2 == 0:
				s += ","
			else:
				s += " "
		else:
			s += i
	return s

def combineSeries(a, b):
	out = []
	for i in range(len(a)):
		out.append(a[i] + b[i])
	return out
		 
def dailyIncrease(l):
	out = []
	for i in range(1, len(l)):
		out.append(int(l[i]) - int(l[i-1]))
	return out	

if __name__ == "__main__": 
	cov = sys.argv[1]
	senti = sys.argv[2]
	#output = sys.argv[2]

	sc=SparkContext("local", "death_trend")
	
	covid = sc.textFile(cov).map(lambda line: parseLine(line).split(",")).filter(lambda line: line[-1].isdigit()).map(lambda line: ["global", dailyIncrease(line[60::])]).reduceByKey(combineSeries).collect()
	covid = sc.parallelize(covid[0][1])
	maximum = covid.max()
	covid = covid.map(lambda each: float(each)/float(maximum))
	covid.saveAsTextFile("covid")
	
	
	sent = sc.textFile(senti).map(lambda line: line.split(" ")).map(lambda line: [int(line[0][14:-4]), float(line[3])]).collect()#.saveAsTextFile("senti_processed")
        sorted_senti = sorted(sent)
	sorted_senti = sc.parallelize(sorted_senti).map(lambda x: x[1])
	max_senti = sorted_senti.max()
	sorted_senti = sorted_senti.map(lambda x: float(x)/float(max_senti))
	sorted_senti.saveAsTextFile("sorted_senti")
        #print(sorted_senti)
	print(Statistics.corr(covid, sorted_senti))
	
