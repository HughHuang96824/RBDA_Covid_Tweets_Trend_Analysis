import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
import datetime
import matplotlib.dates as mdates
import numpy as np
import sys

if __name__ == "__main__":
	day_range = int(sys.argv[1])
	move_forward = int(sys.argv[2])
	covid = []
	senti = []

	smoothed_covid = []
	smoothed_senti = []
	
	
	with open("sorted_senti", "r") as f:
		lines = f.readlines()
		pre = []
		for i, x in enumerate(lines):
			senti.append(float(x))
	
	c = 0
	smoothed_senti = []
	while c < move_forward:
		senti.pop(0)
		c+=1
	pre = []
	for i, x in enumerate(senti):
		x = float(x)
		if i >= day_range-1:
			pre.pop(0)
			pre.append(x)
			smoothed_senti.append(np.mean(pre))
		else:
			pre.append(x)
	             
	with open("covid_death", "r") as f:
		if move_forward != 0:
			lines = f.readlines()[0:-move_forward]
		else: lines = f.readlines()
		pre = []
		for i, x in enumerate(lines):
			x = float(x)
			if i >= day_range-1:
				pre.pop(0)
				pre.append(x)
				smoothed_covid.append(np.mean(pre))
			else:
				pre.append(x)
			covid.append(x)

	print(np.corrcoef(smoothed_senti, smoothed_covid))
	rule = rrulewrapper(YEARLY, byeaster=1, interval=5)
	loc = mdates.MonthLocator()
	formatter = DateFormatter('%m/%d/%y')
	date1 = datetime.date(2020, 3, 20)
	day = 6 - move_forward
	month = 11
	if day <= 0:
		day = 31 + day
		month = 10
	date2 = datetime.date(2020, month, day)
	delta = datetime.timedelta(days=1)
	dates = drange(date1, date2, delta)
	fig, ax = plt.subplots()
	line1, = plt.plot_date(dates, senti, '-', label="Avg Sentiment")
	line2, = plt.plot_date(dates, covid, '-', label = "Death Increase")
	plt.legend(handles = [line1, line2])
	ax.xaxis.set_major_locator(loc)
	ax.xaxis.set_major_formatter(formatter)
	ax.xaxis.set_tick_params(rotation=10, labelsize=10)
	plt.show()

	half_day_range = int((day_range-1)/2)
	fig, ax = plt.subplots()
	line1, = plt.plot_date(dates[day_range-1::], smoothed_senti, '-', label="Smoothed Sentiment")
	line2, = plt.plot_date(dates[day_range-1::], smoothed_covid, '-', label = "Smoothed Death Increase")
	plt.legend(handles = [line1, line2])
	ax.xaxis.set_major_locator(loc)
	ax.xaxis.set_major_formatter(formatter)
	ax.xaxis.set_tick_params(rotation=10, labelsize=10)
	plt.show()

