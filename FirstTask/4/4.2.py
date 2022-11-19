import csv
import re
import prettytable
from prettytable import PrettyTable


class Vacancy:
    number = 1

    def __init__(self, dictionary: dict, headers_array: list):
        self.headers = headers_array
        self.field_dictionary = {}
        if dictionary:
            self.set_vacancy(dictionary)

    def set_vacancy(self, dictionary: dict):
        self.field_dictionary = dictionary
        self.formatter()

    def formatter(self):
        self.delete_html_tags_and_replace_bool_fields()
        self.salary_formatter()

        date = self.field_dictionary["published_at"].split('T')[0].split('-')
        self.field_dictionary['published_at'] = f"{date[2]}.{date[1]}.{date[0]}"

        self.field_dictionary['key_skills'] = self.field_dictionary['key_skills'].replace('; ', '\n')
        self.experience_formatter()

    def delete_html_tags_and_replace_bool_fields(self):
        for key in self.headers:
            value = self.field_dictionary[key]
            value = re.sub('<.*?>', '', str(value)).replace("\r\n", "; ").replace("\n", "; ")
            value = ' '.join(value.split()).strip()
            if value == "False":
                value = "Нет"
            elif value == "True":
                value = "Да"
            self.field_dictionary[key] = value

    def salary_formatter(self):
        salary_from = f'{int(float(self.field_dictionary["salary_from"])):,}'.replace(',', ' ')
        salary_to = f'{int(float(self.field_dictionary["salary_to"])):,}'.replace(',', ' ')

        self.field_dictionary['salary'] = f"{salary_from} - {salary_to} " \
                                    f"({Data_Dictionary.dic_salary_currency[self.field_dictionary['salary_currency']]}) " \
                                    f"{'(С вычетом налогов)' if self.field_dictionary['salary_gross'] != 'Да' else '(Без вычета налогов)'}"

    def experience_formatter(self):
        for field in self.field_dictionary.items():
            key, value = field[0], field[1]
            if value in Data_Dictionary.dic_experience:
                self.field_dictionary[key] = Data_Dictionary.dic_experience[value]

    def is_correct_by_filter(self, filter) -> bool:
        if filter.filter_str == "":
            return True
        else:
            if filter.get_key() == "Оклад":
                return float(self.field_dictionary["salary_from"]) <= float(filter.get_value()) <= float(
                    self.field_dictionary["salary_to"])
            elif filter.get_key() == "Идентификатор валюты оклада":
                return Data_Dictionary.dic_salary_currency[self.field_dictionary['salary_currency']] == filter.get_value()
            elif filter.get_key() == "Навыки":
                for skill in filter.get_value().split(", "):
                    if skill not in self.field_dictionary["key_skills"].split("\n"):
                        return False
                return True
            else:
                inv_dic_filter = {v: k for k, v in Data_Dictionary.dic_filter_for_table.items()}
                return self.field_dictionary[inv_dic_filter[filter.get_key()]] == filter.get_value()

    def get_values_for_table(self):
        values = []
        for field in Data_Dictionary.dic_naming:
            if field == "№":
                values.append(f'{Vacancy.number}')
                Vacancy.number += 1
            else:
                values.append(self.field_dictionary[field])
        return values


class Data_Dictionary:
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

    dic_filter_for_table = {"name": "Название",
                            "description": "Описание",
                            "key_skills": "Навыки",
                            "experience_id": "Опыт работы",
                            "premium": "Премиум-вакансия",
                            "employer_name": "Компания",
                            "salary": "Оклад",
                            "salary_currency": "Идентификатор валюты оклада",
                            "area_name": "Название региона",
                            "published_at": "Дата публикации вакансии"}

    dic_experience = {"noExperience": "Нет опыта",
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


class CSV:
    def csv_reader(file_name: str, filter):
        header_array = []
        vacancies_array = []
        is_empty_file = True
        with open(file_name, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                print("Пустой файл")
                exit()
            header_array = reader.fieldnames
            for row in reader:
                is_empty_file = False
                if all(row.values()):
                    vacancy = Vacancy(row, header_array)
                    if vacancy.is_correct_by_filter(filter):
                        vacancies_array.append(vacancy)
        if is_empty_file:
            print("Нет данных")
            exit()
        return vacancies_array, header_array


class Table:
    def __init__(self):
        self.table = PrettyTable()
        self.table.hrules = prettytable.ALL
        self.table.field_names = Data_Dictionary.dic_naming.values()
        self.table.max_width = 20
        self.table.align = 'l'

    def add_to_table(self, data_vacancies: list):
        count = 0
        for vacancy in data_vacancies:
            count += 1
            row = list(vacancy.get_values_for_table())
            for i in range(len(row)):
                if len(row[i]) > 100:
                    row[i] = row[i][0:100] + '...'
            self.table.add_row(row)

    def print_table(self, indexes: str, field_name: str):
        start_index, end_index, fields_name = self.set_print_settings(indexes, field_name, len(self.table.rows))

        print(self.table.get_string(start=start_index, end=end_index, fields=fields_name))

    def set_print_settings(self, indexes: str, field_name: str, table_size: int):
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


class Filter:
    def __init__(self, filter: str):
        self.filter_str = filter
        if not self.is_correct_filter():
            exit()

    def is_correct_filter(self) -> bool:
        if self.filter_str == "":
            return True
        if ": " not in self.filter_str:
            print("Формат ввода некорректен")
            return False
        for field in Data_Dictionary.dic_filter_for_table.items():
            if self.filter_str.__contains__(field[0]) or self.filter_str.__contains__(field[1]):
                return True
        print("Параметр поиска некорректен")
        return False

    def get_key(self):
        return self.filter_str.split(': ')[0]

    def get_value(self):
        return self.filter_str.split(': ')[1]


file_name = input()
filter_for_table = input()
indexes = input()
field_name = input()

filter = Filter(filter_for_table)

vacancies_array, headers_array = CSV.csv_reader(file_name, filter)

table = Table()

if len(vacancies_array) == 0:
    print("Ничего не найдено")
else:
    table.add_to_table(vacancies_array)
    table.print_table(indexes, field_name)

