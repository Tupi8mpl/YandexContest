import csv
import re
from var_dump import var_dump


def do_exit(message: str):
    print(message)
    exit()


class DataInput:
    def __init__(self):
        self.file_name = input("Введите название файла: ")
        self.filter_for_table = input("Введите параметр фильтрации: ")
        self.parameter_sort = input("Введите параметр сортировки: ")
        self.reverse_sort = input("Обратный порядок сортировки (Да / Нет): ")
        self.indexes = input("Введите диапазон вывода: ").split()
        self.field_name = input("Введите требуемые столбцы: ").split(', ')


class Salary:
    salary_from: str
    salary_to: str
    salary_gross: str
    salary_currency: str


class Vacancy:
    name: str
    description: str
    key_skills: list
    experience_id: str
    premium: str
    employer_name: str
    salary: Salary
    area_name: str
    published_at: str

    def __init__(self, fields):
        for key, value in fields.items():
            value = self.delete_html_tags(value)
            if not self.check_salary(key, value):
                self.__setattr__(key, value)

    def delete_html_tags(self, value: str) -> str:
        value = re.sub('<.*?>', '', str(value)).replace("\r\n", "\n")
        #for skills
        result_array = [' '.join(a.split()) for a in value.split("\n")]
        if len(result_array) == 1:
            return result_array[0]
        return result_array

    def check_salary(self, key: str, value: str) -> bool:
        if key.__contains__("salary"):
            if not hasattr(self, "salary"):
                self.salary = Salary()
            self.salary.__setattr__(key, value)
            return True
        return False


class DataSet:
    def __init__(self, file_name: str, vacancies: list):
        self.file_name = file_name
        self.vacancies_objects = vacancies


class CSV:
    def csv_reader(file_name: str):
        vacancies_array = []
        with open(file_name, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                do_exit("Пустой файл")
            for row in reader:
                if all(row.values()):
                    vacancy = Vacancy(row)
                    vacancies_array.append(vacancy)
        return vacancies_array


user_input = DataInput()
vacancies_array = CSV.csv_reader(user_input.file_name)
data_set = DataSet(user_input.file_name, vacancies_array)

var_dump(data_set)