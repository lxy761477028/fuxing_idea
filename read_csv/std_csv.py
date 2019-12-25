import csv

file1 = r"C:\Users\Farben\Desktop\import.csv"
file2 = r"C:\Users\Farben\Desktop\import1.csv"
file3 = r"C:\Users\Farben\Desktop\import2.csv"

with open(file3, 'r') as f:
    reader = csv.reader(f, delimiter=',')

    # Pick up data line by line
    for i, line in enumerate(reader):
        if i == 0: continue
