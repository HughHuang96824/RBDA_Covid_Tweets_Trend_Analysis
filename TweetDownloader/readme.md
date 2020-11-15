###GetTweet
This part is doing a parallely download and filter of tweet data using Twitter API and spark.

According to Twitter’s Terms of Service, only Tweet IDs of the collected Tweets can be released publicly.
The tweet IDs used for this part is from https://ieee-dataport.org/open-access/coronavirus-covid-19-tweets-dataset

Basically there are four types of tweet according to (https://gwu-libraries.github.io/sfm-ui/posts/2016-11-10-twitter-interaction)
* A tweet
* A tweet that is a retweet
* A tweet that is a quote
* A tweet that is a reply
To avoid repeated counts, we filtered out all the tweets that is a retweet(Since a tweet can be retweeted for many times and the full_text are basically the same).

####requirements:
* [Twitter developer account](https://developer.twitter.com/en/apply-for-access)
* [requests-oauthlib](https://pypi.org/project/requests-oauthlib/#files)
* [pathlib](https://pypi.org/project/pathlib/#files)
* [oauthlib](https://pypi.org/project/oauthlib/#files)
* [twarc](https://github.com/DocNow/twarc)
