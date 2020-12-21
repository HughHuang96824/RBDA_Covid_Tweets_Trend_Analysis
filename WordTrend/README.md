Code to compute and visualize the trending of each word using Spark.  

usage: pyspark unigram_wordTrend.py \<outdir>  \<#topk words to show>  
example: pyspark unigram_wordTrend.py result 100

Barchart_race.py is used to convert our result in to a formatted csv file wich could be accepted by [flourish](https://app.flourish.studio/projects).

### How I preprocess tweets before word count:
* remove tweets that are retweets from dataset
* Remove URLs from tweets.
* Clean up tweet text, including differences in case that will affect unique word counts
* Removing words that are not useful for the analysis using [nltk](https://www.nltk.org/).

### Why do we remove retweets from dataset:
Because the full_text attribute of the Status object may be truncated with an ellipsis
 character instead of containing the full text of the Retweet. Taking retweets in to calculation
 would give wrong reuslts.

### Other thing to be noted:
* The author of datasets we used added more coronavirus specific keywords and the number of tweets captured day has increased significantly, 
Which means there are more tweets collected after April 18. To fix this issue I decided to compute two trends,
before and after April 18.

* The dataset we used do not have covid-related ids before March.
We can use a different dataset from another author: [COVID-19-TweetIDs](https://github.com/echen102/COVID-19-TweetIDs)

* Due to the restriction of tweeter API, we cannot download all the tweets data listed in the id set.
That means we cannot get a complete word trend from Janurary to Now unless we have more time.


### Reference  
[Analyze Word Frequency Counts Using Twitter Data and Tweepy in Python](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/calculate-tweet-word-frequencies-in-python/)  