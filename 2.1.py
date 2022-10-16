import csv


def is_correct_values(values: []) -> bool:
    for value in values:
        if not value:
            return False
    return True


file_name = input()
header_array = []
info_array = []

with open(file_name, 'r', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    header_array = reader.fieldnames
    for row in reader:
        if is_correct_values(row.values()):
            info_array.append(list(row.values()))

print(header_array)
print(info_array)

