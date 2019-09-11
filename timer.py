from sys import argv
from os.path import exists
import csv

csvHeader = ["taskID","taskDesc","timeList"]

def main():
    if len(argv) < 2:
        print("Please provide file name for storage.")
        return
    if exists(argv[1]):
        with open(argv[1], 'r') as storage:
            reader = csv.DictReader(storage)
            for row in reader:
                print(row["timeList"])
            print(str(reader))
    else:
        print("no such file")

if __name__ == "__main__":
    main()
