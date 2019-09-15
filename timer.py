from sys import argv
from os.path import exists
import csv

csvHeader = ["taskID","taskDesc","timeList"]
defaultPrompt = "?>"

def main():
    if len(argv) < 2:
        print("Please provide file name for storage.")
        return
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
                "p" : printAllTasks,
                ":q" : quitSession
             }
    state = {
                "activeTask" : -1,
                "tasks": tasks,
                "prompt" : defaultPrompt
            }
    userQuitSession = False
    while not userQuitSession:
        userInput = input(state["prompt"])
        command,args = splitUserInput(userInput)
        try:
            userQuitSession = switch[command](args, state)
        except:
            continue
    print(tasks)

def readStorageFile(path):
    with open(argv[1], 'r') as storage:
        reader = csv.DictReader(storage)
        for row in reader:
            print(row["timeList"])
    return [],[]

def newTask(args, state):
    print("new task!")
    #stopTask(args, state)
    #newTask = Task(args)
    #state["tasks"].append(newTask)
    #startTask(-1, args)
    state["tasks"].append(args)
    return False

def startTask(args, state):
    try:
        taskId = int(args)
        state["activeTask"] = taskId
        state["prompt"] = state["tasks"][taskId] + defaultPrompt
    except:
        print("invalid task id!")
    return False

def stopTask(args, state):
    if state["activeTask"] > -1:
        state["activeTask"] = -1
        state["prompt"] = defaultPrompt
    return False

def saveState(args, state):
    return False

def printAllTasks(args, state):
    print("printing all tasks!")
    return False

def quitSession(args, state):
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
