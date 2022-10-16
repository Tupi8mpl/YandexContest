import csv
import re
import prettytable
from prettytable import PrettyTable


def is_correct_values(values: []) -> bool:
    for value in values:
        if not value:
            return False
    return True


def csv_reader(file_name: str):
    header_array = []
    vacancies_array = []
    with open(file_name, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        if not reader.fieldnames:
            return vacancies_array, header_array
        header_array = reader.fieldnames
        for row in reader:
            if is_correct_values(row.values()):
                vacancies_array.append(list(row.values()))
    return vacancies_array, header_array


def csv_filer(reader: [], list_naming: []):
    vacancies = []
    for i in range(len(reader)):
        count = 0
        vacancy_dictionary = {}
        for value in reader[i]:
            value = re.sub('<.*?>', '', str(value)).replace("\r\n", ", ").replace("\n", ", ")
            value = ' '.join(value.split()).strip()
            if value == "False":
                value = "Нет"
            elif value == "True":
                value = "Да"
            key = list_naming[count]
            vacancy_dictionary[key] = value
            count = count + 1
        vacancies.append(vacancy_dictionary)
    return vacancies


def salary_formatter(salary_from: str, salary_to: str, salary_currency: str, salary_gross: str):
    salary_from = f'{int(float(salary_from)):,}'.replace(',', ' ')
    salary_to = f'{int(float(salary_to)):,}'.replace(',', ' ')
    return f"{salary_from} - {salary_to}" \
        f" ({salary_currency}) " \
        f"{'(С вычетом налогов)' if salary_gross != 'Да' else '(Без вычета налогов)'}"


def change_salary(row: dict):
    row['salary'] = salary_formatter(row['salary_from'], row['salary_to'],
                                     dic_salary_currency[row['salary_currency']], row['salary_gross'])

    del row['salary_from'], row['salary_to'], row['salary_currency'], row['salary_gross']


def formatter(row: dict) -> dict:
    global dic_expirience, dic_salary_currency

    change_salary(row)

    date = row["published_at"].split('T')[0].split('-')
    row['published_at'] = f"{date[2]}.{date[1]}.{date[0]}"

    row['key_skills'] = row['key_skills'].replace(', ', '\n')
    for field in row.items():
        key, value = field[0], field[1]
        if value in dic_expirience:
            row[key] = dic_expirience[value]
    return row


def add_to_table(table: PrettyTable, data_vacancies: []):
    count = 0
    for dict_vacancy in data_vacancies:
        count += 1
        vacancy = formatter(dict_vacancy)
        row = list(vacancy.values())
        for i in range(len(row)):
            if len(row[i]) > 100:
                row[i] = row[i][0:100] + '...'
        row.insert(0, count)
        row[7], row[8], row[9] = row[9], row[7], row[8]
        table.add_row(row)


def print_table(table: PrettyTable, indexes: str, field_name: str):
    start_index, end_index, fields_name = set_print_settings(indexes, field_name, len(table.rows))

    print(table.get_string(start=start_index, end=end_index, fields=fields_name))


def set_print_settings(indexes: str, field_name: str, table_size: int):
    fields_name = ("№, " + field_name).split(', ')
    end_index = table_size
    if indexes == '':
        start_index = 0
    elif indexes.__contains__(' '):
        indexes_array = indexes.split(' ')
        start_index, end_index = int(indexes_array[0]) - 1, int(indexes_array[1]) - 1
    else:
        start_index = int(indexes) - 1

    if field_name == '':
        fields_name = ''
    return start_index, end_index, fields_name


table = PrettyTable()
table.hrules = prettytable.ALL
dic_naming = {"№": "№",
              "name": "Название",
              "description": "Описание",
              "key_skills": "Навыки",
              "experience_id": "Опыт работы",
              "premium": "Премиум-вакансия",
              "employer_name": "Компания",
              "salary": "Оклад",
              "area_name": "Название региона",
              "published_at": "Дата публикации вакансии"}
table.field_names = dic_naming.values()
table.max_width = 20
table.align = 'l'

dic_expirience = {"noExperience": "Нет опыта",
                  "between1And3": "От 1 года до 3 лет",
                  "between3And6": "От 3 до 6 лет",
                  "moreThan6": "Более 6 лет"}

dic_salary_currency = {"AZN": "Манаты",
                       "BYR": "Белорусские рубли",
                       "EUR": "Евро",
                       "GEL": "Грузинский лари",
                       "KZT": "Тенге",
                       "RUR": "Рубли",
                       "UAH": "Гривны",
                       "USD": "Доллары",
                       "UZS": "Узбекский сум"}


file_name = input()
indexes = input()
field_name = input()

vacancies_array, headers_array = csv_reader(file_name)
if len(headers_array) == 0:
    print("Пустой файл")
elif len(vacancies_array) == 0:
    print("Нет данных")
else:
    vacancies_dictionary = csv_filer(vacancies_array, headers_array)
    add_to_table(table, vacancies_dictionary)
    print_table(table, indexes, field_name)