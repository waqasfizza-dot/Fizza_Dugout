import csv

with open("data\\players.csv", newline="",encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row)
        break