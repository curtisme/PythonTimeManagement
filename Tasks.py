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
        self.timeList, self.errors = getTimes(timeListString)


