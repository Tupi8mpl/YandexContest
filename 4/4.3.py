import csv
import re
import prettytable
from prettytable import PrettyTable
from datetime import datetime


def do_exit(message: str):
    print(message)
    exit()


class Vacancy:
    number = 1

    def __init__(self, dictionary: dict, headers_array: list):
        self.headers = headers_array
        self.field_dictionary = {}
        self.date_time_publishing = None
        self.inv_dic_filter = {v: k for k, v in Data_Dictionary.dic_filter_for_table.items()}
        if dictionary:
            self.set_vacancy(dictionary)

    def set_vacancy(self, dictionary: dict):
        self.field_dictionary = dictionary
        self.formatter()

    def formatter(self):
        self.delete_html_tags_and_replace_bool_fields()
        self.salary_formatter()

        self.published_time_formatter()

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

    def published_time_formatter(self):
        hour, minute, second = self.field_dictionary["published_at"].split('T')[1].split('+')[0].split(':')
        year, month, day = self.field_dictionary["published_at"].split('T')[0].split('-')
        self.date_time_publishing = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        self.field_dictionary['published_at'] = f"{day}.{month}.{year}"

    def experience_formatter(self):
        for field in self.field_dictionary.items():
            key, value = field[0], field[1]
            if value in Data_Dictionary.dic_experience:
                self.field_dictionary[key] = Data_Dictionary.dic_experience[value]

    def is_correct_by_filter(self, filter: str) -> bool:
        if filter == "":
            return True
        else:
            temp = filter.split(": ")
            key, value = temp[0], temp[1]
            if key == "Оклад":
                return float(self.field_dictionary["salary_from"]) <= float(value) <= float(
                    self.field_dictionary["salary_to"])
            elif key == "Идентификатор валюты оклада":
                return Data_Dictionary.dic_salary_currency[
                           self.field_dictionary['salary_currency']] == value
            elif key == "Навыки":
                for skill in value.split(", "):
                    if skill not in self.field_dictionary["key_skills"].split("\n"):
                        return False
                return True
            else:
                return self.field_dictionary[self.inv_dic_filter[key]] == value

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

    dix_experience_to_int = {"Нет опыта": 0,
                             "От 1 года до 3 лет": 2,
                             "От 3 до 6 лет": 4,
                             "Более 6 лет": 6}

    dic_experience_sort = {"noExperience": "Нет опыта",
                           "between1And3": "От 1 года до 3 лет",
                           "between3And6": "От 3 до 6 лет",
                           "moreThan6": "Более 6 лет"}

    dic_salary_currency = {"AZN": "Манаты",
                           "BYR": "Белорусские рубли",
                           "EUR": "Евро",
                           "GEL": "Грузинский лари",
                           "KZT": "Тенге",
                           "KGS": "Киргизский сом",
                           "RUR": "Рубли",
                           "UAH": "Гривны",
                           "USD": "Доллары",
                           "UZS": "Узбекский сум"}

    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }


class CSV:
    def csv_reader(file_name: str, filter: str):
        header_array = []
        vacancies_array = []
        is_empty_file = True
        with open(file_name, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                do_exit("Пустой файл")
            header_array = reader.fieldnames
            for row in reader:
                is_empty_file = False
                if all(row.values()):
                    vacancy = Vacancy(row, header_array)
                    if vacancy.is_correct_by_filter(filter):
                        vacancies_array.append(vacancy)
        if is_empty_file:
            do_exit("Нет данных")
        return vacancies_array, header_array

    def sorting_vacancies(vacancies_array: list, parameter_sort: str, reverse_sort: str):
        if parameter_sort == "":
            return True
        else:
            is_reverse = reverse_sort == "Да"
            sort_lambda = None
            if parameter_sort == "Оклад":
                sort_lambda = lambda vacancy: (float(vacancy.field_dictionary["salary_to"]) *
                                               Data_Dictionary.currency_to_rub[
                                                   vacancy.field_dictionary["salary_currency"]] +
                                               float(vacancy.field_dictionary["salary_from"]) *
                                               Data_Dictionary.currency_to_rub[
                                                   vacancy.field_dictionary["salary_currency"]]) // 2
            elif parameter_sort == "Навыки":
                sort_lambda = lambda vacancy: len(vacancy.field_dictionary["key_skills"].split("\n"))
            elif parameter_sort == "Дата публикации вакансии":
                sort_lambda = lambda vacancy: vacancy.date_time_publishing
            elif parameter_sort == "Опыт работы":
                sort_lambda = lambda vacancy: Data_Dictionary.dix_experience_to_int[
                    vacancy.field_dictionary["experience_id"]]
            else:
                sort_lambda = lambda vacancy: vacancy.field_dictionary[vacancy.inv_dic_filter[parameter_sort]]
            vacancies_array.sort(reverse=is_reverse, key=sort_lambda)


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


def is_correct_filter(filter: str):
    if filter == "":
        return
    if ": " not in filter:
        do_exit("Формат ввода некорректен")
    for field in Data_Dictionary.dic_filter_for_table.items():
        if filter.__contains__(field[0]) or filter.__contains__(field[1]):
            return
    do_exit("Параметр поиска некорректен")


def is_correct_parameter_sort(parametr_sort: str):
    if not parametr_sort:
        return
    if parameter_sort not in Data_Dictionary.dic_naming.values():
        do_exit("Параметр сортировки некорректен")


def is_correct_reverse_sort(reverse_sort: str):
    if not reverse_sort:
        return
    if reverse_sort != "Да" and reverse_sort != "Нет":
        do_exit("Порядок сортировки задан некорректно")


file_name = input("Введите название файла: ")
filter_for_table = input("Введите параметр фильтрации: ")
parameter_sort = input("Введите параметр сортировки: ")
reverse_sort = input("Обратный порядок сортировки (Да / Нет): ")
indexes = input("Введите диапазон вывода: ")
field_name = input("Введите требуемые столбцы: ")

is_correct_filter(filter_for_table)
is_correct_parameter_sort(parameter_sort)
is_correct_reverse_sort(reverse_sort)

vacancies_array, headers_array = CSV.csv_reader(file_name, filter_for_table)

table = Table()

if len(vacancies_array) == 0:
    do_exit("Ничего не найдено")
else:
    CSV.sorting_vacancies(vacancies_array, parameter_sort, reverse_sort)
    table.add_to_table(vacancies_array)
    table.print_table(indexes, field_name)
