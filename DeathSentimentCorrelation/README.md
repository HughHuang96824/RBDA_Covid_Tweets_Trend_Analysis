Put time_series_covid19_deaths_global and avg_senti to hdfs

run

 "pyspark death_data_total.py time_series_covid19_deaths_global avg_senti"

It will generate covid/part-00000 and sorted_senti/part-00000 files (covid_death and sorted_senti files in this directory) and print the correlation between two series.

run

"python plotSentiCovid.py x y", where x is the number of days you want to take average of and y is the number of days you want to move sentiment time series forwards by

to get plots



