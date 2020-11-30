#### This code is used to compute the total number of tweets on each day, and the average sentiment score on each day

usage: spark-submit --driver-memory 4g getAverage.py <local input directory> <local output path>
example: spark-submit --driver-memory 4g getAverage.py all-data avg_res
