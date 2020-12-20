create_at = "Wed Apr 01 05:19:10 +0000 2020"

def parse(create_at):
    timeDict = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"}
    times = create_at.split(" ")
    month = timeDict[times[1]]
    day = times[2]
    return month + day