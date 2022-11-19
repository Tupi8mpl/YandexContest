import csv
import re
import math


def is_correct_values(values: []) -> bool:
    for value in values:
        if not value:
            return False
    return True


def refactor_values(row: dict):
    for key in row.keys():
        row[key] = re.sub('<.*?>', '', row[key])
        row[key] = row[key].replace("\r\n", ", ").replace("\n", ", ")
        row[key] = ' '.join(row[key].split()).strip()
        print(f"{key.strip()}: {row[key]}")


file_name = input()
with open(file_name, 'r', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if is_correct_values(row.values()):
            refactor_values(row)
            print()