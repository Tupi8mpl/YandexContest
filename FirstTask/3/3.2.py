import csv
import re
import math
import datetime

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
            count = (count + 1) % len(list_naming)
        vacancies.append(vacancy_dictionary)
    return vacancies


def salary_formatter(salary_from: str, salary_to: str, salary_currency: str, salary_gross: str):
    salary_from = f'{int(float(salary_from)):,}'.replace(',', ' ')
    salary_to = f'{int(float(salary_to)):,}'.replace(',', ' ')
    return f"{salary_from} - {salary_to}" \
        f" ({salary_currency}) " \
        f"{'(С вычетом налогов)' if salary_gross != 'Да' else '(Без вычета налогов)'}"

def formatter(row: dict):
    global dic_expirience, dic_salary_currency
    row['salary'] = salary_formatter(row['salary_from'], row['salary_to'],
                         dic_salary_currency[row['salary_currency']], row['salary_gross'])

    del row['salary_from'], row['salary_to'], row['salary_currency'], row['salary_gross']

    date = row["published_at"].split('T')[0].split('-')
    row['published_at'] = f"{date[2]}.{date[1]}.{date[0]}"
    for field in row.items():
        if field[1] in dic_expirience:
            row[field[0]] = dic_expirience[field[1]]
    return row


def print_vacancies(data_vacancies: [], dic_naming: dict):
    for dict_vacancy in data_vacancies:
        vacancy = formatter(dict_vacancy)
        for row in dic_naming.items():
            print(f"{row[1]}: {vacancy[row[0]]}")
        print()


dic_naming = {"name": "Название",
              "description": "Описание",
              "key_skills": "Навыки",
              "experience_id": "Опыт работы",
              "premium": "Премиум-вакансия",
              "employer_name": "Компания",
              "salary": "Оклад",
              "area_name": "Название региона",
              "published_at": "Дата публикации вакансии"}

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
vacancies_array, headers_array = csv_reader(input())
vacancies_dictionary = csv_filer(vacancies_array, headers_array)
print_vacancies(vacancies_dictionary, dic_naming)