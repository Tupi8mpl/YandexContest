import csv
import re
import prettytable
from prettytable import PrettyTable
from datetime import datetime


def do_exit(message: str):
    print(message)
    exit()


class InputConnect:
    def __init__(self):
        self.file_name = input("Введите название файла: ")
        self.filter_for_table = input("Введите параметр фильтрации: ")
        self.parameter_sort = input("Введите параметр сортировки: ")
        self.reverse_sort = input("Обратный порядок сортировки (Да / Нет): ")
        self.indexes = input("Введите диапазон вывода: ")
        self.field_name = input("Введите требуемые столбцы: ")
        self.input_validation()

    def input_validation(self):
        self.is_correct_filter()
        self.is_correct_parameter_sort()
        self.is_correct_reverse_sort()

    def is_correct_filter(self):
        if self.filter_for_table == "":
            return
        if ": " not in self.filter_for_table:
            do_exit("Формат ввода некорректен")
        for field in DataDictionary.dic_filter_for_table.items():
            if self.filter_for_table.__contains__(field[0]) or self.filter_for_table.__contains__(field[1]):
                return
        do_exit("Параметр поиска некорректен")

    def is_correct_parameter_sort(self):
        if not self.parameter_sort:
            return
        if self.parameter_sort not in DataDictionary.dic_naming.values():
            do_exit("Параметр сортировки некорректен")

    def is_correct_reverse_sort(self):
        if not self.reverse_sort:
            return
        if self.reverse_sort != "Да" and self.reverse_sort != "Нет":
            do_exit("Порядок сортировки задан некорректно")


class Salary:
    salary_from: str
    salary_to: str
    salary_gross: str
    salary_currency: str
    salary_string: str

    def set_salary_string(self):
        salary_from = f'{int(float(self.salary_from)):,}'.replace(',', ' ')
        salary_to = f'{int(float(self.salary_to)):,}'.replace(',', ' ')

        self.salary_string = f"{salary_from} - {salary_to} " \
                             f"({DataDictionary.dic_salary_currency[self.salary_currency]}) " \
                             f"{'(С вычетом налогов)' if self.salary_gross != 'Да' else '(Без вычета налогов)'}"


class Vacancy:
    number = 1
    name: str
    description: str
    key_skills: list
    experience_id: str
    premium: str
    employer_name: str
    salary: Salary
    area_name: str
    published_at: str

    def __init__(self, fields: dict):
        self.inv_dic_filter = {v: k for k, v in DataDictionary.dic_filter_for_table.items()}
        self.date_time_publishing = None
        for key, value in fields.items():
            value = self.delete_html_tags(key, value)
            value = self.replace_bool_fields(value)
            if not self.check_salary(key, value):
                self.__setattr__(key, value)

        self.published_time_formatter()
        self.salary.set_salary_string()
        self.experience_formatter()

    def delete_html_tags(self, key: str, value: str) -> str:
        value = re.sub('<.*?>', '', str(value)).replace("\r\n", "; ").replace("\n", "; ")
        value = ' '.join(value.split()).strip()
        #for skills
        if key != "key_skills":
            return value
        result_array = [a for a in value.split("; ")]
        return result_array

    def replace_bool_fields(self, value: str):
        if value == "False":
            value = "Нет"
        elif value == "True":
            value = "Да"
        return value

    def check_salary(self, key: str, value: str) -> bool:
        if key.__contains__("salary"):
            if not hasattr(self, "salary"):
                self.salary = Salary()
            self.salary.__setattr__(key, value)
            return True
        return False

    def published_time_formatter(self):
        hour, minute, second = self.published_at.split('T')[1].split('+')[0].split(':')
        year, month, day = self.published_at.split('T')[0].split('-')
        self.date_time_publishing = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        self.published_at = f"{day}.{month}.{year}"

    def experience_formatter(self):
        if self.experience_id in DataDictionary.dic_experience:
            self.experience_id = DataDictionary.dic_experience[self.experience_id]

    def is_correct_by_filter(self, filter: str) -> bool:
        if filter == "":
            return True
        else:
            temp = filter.split(": ")
            key, value = temp[0], temp[1]
            if key == "Оклад":
                return float(self.salary.salary_from) <= float(value) <= float(
                    self.salary.salary_to)
            elif key == "Идентификатор валюты оклада":
                return DataDictionary.dic_salary_currency[
                           self.salary.salary_currency] == value
            elif key == "Навыки":
                for skill in value.split(", "):
                    if skill not in self.key_skills:
                        return False
                return True
            else:
                return self.__getattribute__(self.inv_dic_filter[key]) == value

    def get_values_for_table(self):
        values = []
        for field in DataDictionary.dic_naming:
            if field == "№":
                values.append(f'{Vacancy.number}')
                Vacancy.number += 1
            elif field == "key_skills":
                values.append('\n'.join(self.key_skills))
            elif field == "salary":
                values.append(self.salary.salary_string)
            else:
                values.append(self.__getattribute__(field))
        return values


class DataDictionary:
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


class DataSet:
    def csv_reader(file_name: str, filter: str):
        vacancies_array = []
        is_empty_file = True
        with open(file_name, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                do_exit("Пустой файл")
            for row in reader:
                is_empty_file = False
                if all(row.values()):
                    vacancy = Vacancy(row)
                    if vacancy.is_correct_by_filter(filter):
                        vacancies_array.append(vacancy)
        if is_empty_file:
            do_exit("Нет данных")
        return vacancies_array

    def sorting_vacancies(vacancies_array: list, parameter_sort: str, reverse_sort: str):
        if parameter_sort == "":
            return True
        else:
            is_reverse = reverse_sort == "Да"
            sort_lambda = None
            if parameter_sort == "Оклад":
                sort_lambda = lambda vacancy: (float(vacancy.salary.salary_to) *
                                               DataDictionary.currency_to_rub[
                                                   vacancy.salary.salary_currency] +
                                               float(vacancy.salary.salary_from) *
                                               DataDictionary.currency_to_rub[
                                                   vacancy.salary.salary_currency]) // 2
            elif parameter_sort == "Навыки":
                sort_lambda = lambda vacancy: len(vacancy.key_skills)
            elif parameter_sort == "Дата публикации вакансии":
                sort_lambda = lambda vacancy: vacancy.date_time_publishing
            elif parameter_sort == "Опыт работы":
                sort_lambda = lambda vacancy: DataDictionary.dix_experience_to_int[
                    vacancy.experience_id]
            else:
                sort_lambda = lambda vacancy: vacancy.__getattribute__(vacancy.inv_dic_filter[parameter_sort])
            vacancies_array.sort(reverse=is_reverse, key=sort_lambda)


class Table:
    def __init__(self):
        self.table = PrettyTable()
        self.table.hrules = prettytable.ALL
        self.table.field_names = DataDictionary.dic_naming.values()
        self.table.max_width = 20
        self.table.align = 'l'

    def add_to_table(self, data_vacancies: list):
        for vacancy in data_vacancies:
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


user_input = InputConnect()
vacancies_array = DataSet.csv_reader(user_input.file_name, user_input.filter_for_table)

table = Table()

if len(vacancies_array) == 0:
    do_exit("Ничего не найдено")
else:
    DataSet.sorting_vacancies(vacancies_array, user_input.parameter_sort, user_input.reverse_sort)
    table.add_to_table(vacancies_array)
    table.print_table(user_input.indexes, user_input.field_name)