import csv
import json
from datetime import datetime


def addModificationToTree(treeUp, lstData):
    """
        Add a directory string list group into the tree structure
    """

    # Whenever we add a file into a set of directory, increase the count of all directories
    treeUp[0] += 1

    # getting this level from the directory group, if not exist initiate it
    data = lstData.pop(0)
    if data not in treeUp[1]:
        treeUp[1][data] = [0, {}]

    # Recursively add the popped group of directories
    if len(lstData) != 0:
        addModificationToTree(treeUp[1][data], lstData)


def isWithinDate(date, dateStart, dateEnd):
    return dateStart <= date <= dateEnd


def main(hostname, filenameIn, filenameOut, dateStart, dateEnd):
    """
        Main function of the script
    """

    # Read the CSV File
    with open(filenameIn, mode="r", newline="\n") as fileInput:
        objReader = csv.reader(fileInput)

        next(objReader)     # Skip header wor
        cptOut = 0
        cptIn = 0
        treeModifications = [0, {}]
        while True:
            cptIn += 1
            if cptIn % 1000 == 0:
                print(f"Processed In: {cptIn}")

            try:
                row = next(objReader)
            except StopIteration as e1:
                # Normal End, quit the loop
                break
            except BaseException as e:
                # Rare error where there is a NUL character in the csv
                print(e)
                if e.args[0] == "line contains NUL":
                    continue

            #ProcessFilteringByDate
            isIn = False
            for i in range(8, 16):
                try:
                    dateToTest = datetime.strptime(row[i], "%Y-%m-%d %H:%M:%S.%f")
                    if isWithinDate(dateToTest, dateStart, dateEnd):
                        isIn = True
                except ValueError as e:
                    continue
                except IndexError as e:
                    continue

            if not isIn:
                continue

            #filter by isDirectory
            if row[3][1] != "i":
                continue

            #filter by isInUsed
            if row[2][0] != "A":
                continue

            #filter by fileSizeIsZero



            # Initiate the tree with the hostname
            addModificationToTree(treeModifications, [hostname])

            # Then column 0 contains the full path where we organize in tree
            groupFolder = row[7].split("/")
            addModificationToTree(treeModifications[1][hostname], groupFolder)

            # Debug information to show that things are still running
            cptOut += 1
            if cptOut % 100 == 0:
                print(f"\t\t\tProcessed Out: {cptOut}")

        print(f"Completed!!")
        # Output a dump of the Dictionary as JSON
        with open(filenameOut, mode="w", newline="\n") as fileOutput:
            json.dump({"data": treeModifications}, fileOutput)


if __name__ == '__main__':
    main("JF", f"./data/output_968.csv", f"./data/output_968.json",
         datetime.strptime("2017-07-28T10:00:00.000000", "%Y-%m-%dT%H:%M:%S.%f"),
         datetime.strptime("2017-07-28T11:00:00.000000", "%Y-%m-%dT%H:%M:%S.%f"))

    main("JF", f"./data/output_212569.csv", f"./data/output_212569.json",
         datetime.strptime("2021-06-07T09:30:00.000000", "%Y-%m-%dT%H:%M:%S.%f"),
         datetime.strptime("2021-06-07T10:30:00.000000", "%Y-%m-%dT%H:%M:%S.%f"))
