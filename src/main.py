import csv
import json


def addModificationToTree(treeUp, lstData):
    treeUp[0] += 1
    data = lstData.pop(0)

    if data not in treeUp[1]:
        treeUp[1][data] = [0, {}]

    if len(lstData) != 0:
        addModificationToTree(treeUp[1][data], lstData)


def main():
    # Read the CSV File
    with open(f"./data/query_1(2).csv", mode="r", newline="\n") as fileInput:
        objReader = csv.reader(fileInput)

        next(objReader)
        # For each row, get row[1]
        cpt = 0
        treeModifications = [0, {}]
        while True:
            try:
                row = next(objReader)
            except StopIteration as e1:
                break
            except BaseException as e:
                print(e)
                if e.args[0] == "line contains NUL":
                    continue

            hostname = row[7]
            addModificationToTree(treeModifications, [hostname])

            groupFolder = row[0].split("\\")
            addModificationToTree(treeModifications[1][hostname], groupFolder)

            cpt += 1

            if cpt % 1000 == 0:
                print(f"Processed {cpt}")

        # print(treeModifications)
        with open(f"./data/output.json", mode="w", newline="\n") as fileOutput:
            json.dump({"data": treeModifications}, fileOutput)


if __name__ == '__main__':
    main()
