###HeatMapGenerator

####Download geo-tagged tweets
Use geoExtractor.py with [geo-tagged-tweets-dataset](https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset).
This program will parse the tweet id from the dataset, use if to hydrate all the tweets, and extract the info we need to draw a heat map.
Usage: pyspark geoExtractor.py \<path1> \<path2>  
\<path1>: local directory path of the 
\<path2>: hdfs output path
example: pyspark geoExtractor.py geo-data /user/ja3802/geo-tweets


####compute HeatMap data using spark
Use getHeatMapData.py to process the downloaded tweets.
This program will join the sentiment score of each tweets by id, and partition the tweets by the dates they were created.  
Usage: pyspark getHeatMapData.py \<path1> \<path2>  
\<path1>: hdfs path of all the downloaded data  
\<path2>: hdfs path of all the source dataset
example: pyspark getHeatMapData.py /user/ja3802/geo_tweets/\*/* /user/ja3802/geo-data/*
