### GetTweet
This part is doing a parallely download and filter of tweet data using Twitter API and spark.

According to Twitter’s Terms of Service, only Tweet IDs of the collected Tweets can be released publicly.
The tweet IDs used for this part is from https://ieee-dataport.org/open-access/coronavirus-covid-19-tweets-dataset

Basically there are four types of tweet according to (https://gwu-libraries.github.io/sfm-ui/posts/2016-11-10-twitter-interaction)
* A tweet
* A tweet that is a retweet
* A tweet that is a quote
* A tweet that is a reply

To avoid repeated counts, we filtered out all the tweets that is a retweet(Since a tweet can be retweeted for many times and the full_text are basically the same).
And we keep all the number of likes and retweets for a retweet, quote or a reply.

#### requirements:
* [Twitter developer account](https://developer.twitter.com/en/apply-for-access)
* [requests-oauthlib](https://pypi.org/project/requests-oauthlib/#files)
* [pathlib](https://pypi.org/project/pathlib/#files)
* [oauthlib](https://pypi.org/project/oauthlib/#files)
* [twarc](https://github.com/DocNow/twarc)

### 11/16:
To avoid out of memory error, we choose to process 20000 tweets and store result into HDFS per loop.
Due to the restriction of twitter API, User Auth can only issue 180 requests every 15 minutes (1.6 million tweets per day), and App Auth can issue 450 (4.3 million tweets per day).
According to my calculation and estimation, our program is processing 5200 tweets/min.

### 11/22:
Switched from User Auth to App auth. The speed now is 13000 tweets/min.