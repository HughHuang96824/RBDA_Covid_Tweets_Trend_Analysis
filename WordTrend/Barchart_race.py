import csv
import datetime


headers = ['word']

rows = []


unigram_dir = r"P:\NYU\RBDA\FinalProject\RBDA_Covid_Tweets_Trend_Analysis\WordTrend\result"

dict = {}
word_id = 0
for i in range(1,59):
    fname = unigram_dir + "\\" + str(i)
    with open(fname, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            l = l.rstrip("\n")[1:-1].split(",")
            score = int(l[0])
            word = l[1][3:-1].encode('unicode-escape').replace(b'\\\\', b'\\').decode('unicode-escape')
            if word[0] in ["“"]:
                word = word[1:]
            if word[-1] in [":", "”"]:
                word = word[:-1]
            if not rows:
                print(word)
                rows.append([word]+[0]*58)
                rows[0][i] = score
                dict[word] = word_id
            else:
                if word in dict.keys():
                    rows[dict[word]][i] = score
                else:
                    rows.append([word] + [0]*58)
                    word_id += 1
                    rows[-1][i] = score
                    dict[word] = word_id

print(dict)

#days
d1 = datetime.date(2020, 3, 18)
d2 = datetime.date(2020, 5, 14)
days = [d1 + datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]
headers += days

#remove keywords
keyword = ['covid', 'corona', "virus", 'coronavirus', 'covid-19', "covid19"]

for r in rows:
    #print(r[0])
    if len(r[0]) == 1:
        rows.remove(r)
    else:
        if r[0] in keyword:
            rows.remove(r)

with open('race.csv','w')as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    for i in range(len(rows)):
        try:
            f_csv.writerow(rows[i])
        except:
            continue
