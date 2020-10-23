from sys import argv
from os.path import exists
from Tasks import Task
import os
import csv

csvHeader = ["taskDesc","timeList", "comments"]
defaultPrompt = "?> "
clearCommand = "cls" if os.name == "nt" else "clear"
isReadOnly = False

def main():
    if len(argv) < 2:
        print("Please provide file name for storage.")
        return
    if len(argv) > 2:
        global isReadOnly
        isReadOnly = argv[2] == "r"
    clearScreen()
    if isReadOnly:
        print("Application open in Read Only mode.")
    tasks = []
    if exists(argv[1]):
        tasks,errors = readStorageFile(argv[1])
        if errors:
            print(errors[0])
    switch = {
                "n" : newTask,
                "s" : startTask,
                "x" : stopTask,
                "b" : saveState,
                "p" : printTask,
                ":c" : clearScreen,
                ":q" : quitSession
             }
    state = {
                "activeTask" : -1,
                "tasks": tasks,
                "prompt" : defaultPrompt,
                "storagePath" : argv[1]
            }
    userQuitSession = False
    while not userQuitSession:
        userInput = input(state["prompt"])
        command,args = splitUserInput(userInput)
        try:
            userQuitSession = switch[command](args, state)
        except KeyError:
            continue

def readStorageFile(path):
    taskList = []
    errors = []
    with open(argv[1], 'r') as storage:
        reader = csv.DictReader(storage)
        if (reader.fieldnames == csvHeader):
            for row in reader:
                newTask = Task(row["taskDesc"], row["timeList"], row["comments"])
                taskList.append(newTask)
        else:
            errors.append("Incorrect header format in {}".format(path))
    return taskList, errors

def newTask(args, state):
    state["tasks"].append(Task(args))
    startTask(-1, state)
    return False

def startTask(args, state):
    stopTask(args, state)
    try:
        taskId = int(args)
        state["tasks"][taskId].start()
        state["activeTask"] = taskId if taskId > -1 else len(state["tasks"]) - 1
        state["prompt"] = state["tasks"][taskId].description + defaultPrompt
    except:
        print("invalid task id!")
    return False

def stopTask(args, state):
    if state["activeTask"] > -1:
        state["tasks"][state["activeTask"]].stop()
        state["activeTask"] = -1
        state["prompt"] = defaultPrompt
    return False

def saveState(args, state):
    if not isReadOnly:
        stopTask(args, state)
        with open(state["storagePath"], "w") as storage:
            writer = csv.DictWriter(storage, csvHeader)
            writer.writeheader()
            for task in state["tasks"]:
                writer.writerow({"taskDesc" : task.description,"timeList" : task.timeListToString(),"comments": ""})
    return False

def printTask(args, state):
    try:
        taskID = int(args)
        print("taskId: {}, {}".format(taskID, state["tasks"][taskID]))
    except:
        for i in range(len(state["tasks"])):
            print("taskId: {}, {}".format(i, state["tasks"][i].description))
    return False

def clearScreen(*args):
    os.system(clearCommand)
    return False

def quitSession(args, state):
    saveState(args, state)
    return True

def splitUserInput(userInput):
    pos = 0
    for c in userInput:
        if c == ' ':
            break
        pos += 1
    return userInput[:pos], userInput[pos+1:]

if __name__ == "__main__":
    main()
