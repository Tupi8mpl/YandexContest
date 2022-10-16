import csv
import re


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

def print_vacancies(data_vacancies: [], dic_naming: dict):
    for vacancy in data_vacancies:
        for row in vacancy.items():
            print(f"{dic_naming[row[0]]}: {row[1]}")
        print()


dic_naming = {"name": "Название",
              "description": "Описание",
              "key_skills": "Навыки",
              "experience_id": "Опыт работы",
              "premium": "Премиум-вакансия",
              "employer_name": "Компания",
              "salary_from": "Нижняя граница вилки оклада",
              "salary_to": "Верхняя граница вилки оклада",
              "salary_gross": "Оклад указан до вычета налогов",
              "salary_currency": "Идентификатор валюты оклада",
              "area_name": "Название региона",
              "published_at": "Дата и время публикации вакансии"}
vacancies_array, headers_array = csv_reader(input())
vacancies_dictionary = csv_filer(vacancies_array, headers_array)
print_vacancies(vacancies_dictionary, dic_naming)