from time import time as now
from time import localtime

class Task:
    def __init__(self, taskDesc, timeListString = "", commentsString = ""):
        def getTimes(timeListString):
            timeList = []
            errors = []
            if timeListString:
                intervals = timeListString.split('|')
                for interval in intervals:
                    try:
                        times = list(map(int, interval.split(':')))
                    except:
                        errors.append("Error in interval {}. Can't read int!".format(interval))
                        timeList = []
                        break
                    if times[0] >= times[1] or timeList and timeList[-1][1] >= times[0]:
                        errors.append("big poop")
                        timeList = []
                        break
                    timeList.append(times)
            return timeList, errors
        self.description = taskDesc
        #self.timeList, self.errors = getTimes(timeListString)
        self.timeList, self.errors = [], []
        self.active = False

    def start(self):
        if not self.active:
            self.timeList.append([int(now()), -1])
            self.active = True


    def stop(self):
        if self.active:
            self.timeList[-1][1] = int(now())
            self.active = False

    def __str__(self):
        out = "{}:\n".format(self.description)
        for time in self.timeList:
            start = localtime(time[0])
            if time[1] != -1:
                stop = localtime(time[1])
                endString = "{}:{}.{}".format(stop.tm_hour, stop.tm_min, stop.tm_sec)
            else:
                endString = "?"
            out += "{}:{}.{} - {}\n".format(start.tm_hour, start.tm_min, start.tm_sec, endString)
        return out
    
    def toCSVRow(self):
        timeList = ""
        for time in self.timeList:
            timeList += "{}:{}|".format(time[0], time[1])
        return "{},{}".format(self.description, timeList)

