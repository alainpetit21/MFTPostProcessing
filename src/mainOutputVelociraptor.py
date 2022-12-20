import csv
import json


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


def main():
    """
        Main function of the script
    """

    # Read the CSV File
    with open(f"./data/DeletedFiles_E.csv", mode="r", newline="\n") as fileInput:
        objReader = csv.reader(fileInput)

        next(objReader)     # Skip header wor
        cpt = 0
        treeModifications = [0, {}]
        while True:
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

            # Initiate the tree with the hostname
            hostname = row[7]
            addModificationToTree(treeModifications, [hostname])

            # Then column 0 contains the full path where we organize in tree
            groupFolder = row[0].split("\\")
            addModificationToTree(treeModifications[1][hostname], groupFolder)

            # Debug information to show that things are still running
            cpt += 1
            if cpt % 1000 == 0:
                print(f"Processed {cpt}")

        # Output a dump of the Dictionary as JSON
        with open(f"./data/output.json", mode="w", newline="\n") as fileOutput:
            json.dump({"data": treeModifications}, fileOutput)


if __name__ == '__main__':
    main()
