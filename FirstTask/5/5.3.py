import csv
import re
from datetime import datetime


def do_exit(message: str):
    print(message)
    exit()


class UserInput:
    def __init__(self):
        self.file_name = input("Введите название файла: ")
        self.profession = input("Введите название профессии: ")


class Salary:
    salary_from: str
    salary_to: str
    salary_currency: str
    average_salary: int
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

    def set_attribute(self, key: str, value: str):
        if key == "salary_gross":
            return
        if key != 'salary_currency':
            value = float(value)
        self.__setattr__(key, value)

    def set_average_salary(self):
        self.average_salary = int(self.currency_to_rub[self.salary_currency] *
                                  (float(self.salary_from) + float(self.salary_to)) // 2)


class Vacancy:
    name: str
    employer_name: str
    salary: Salary
    area_name: str
    published_at: int

    def __init__(self, fields: dict):
        self.date_time_publishing = None
        for key, value in fields.items():
            value = self.delete_html_tags(value)
            if not self.check_salary(key, value):
                self.__setattr__(key, value)

        self.published_time_formatter()
        self.salary.set_average_salary()

    def delete_html_tags(self, value: str) -> str:
        value = re.sub('<.*?>', '', str(value)).replace("\r\n", "\n")
        value = ' '.join(value.split()).strip()
        return value

    def check_salary(self, key: str, value: str) -> bool:
        if not key.__contains__("salary"):
            return False
        if not hasattr(self, "salary"):
            self.salary = Salary()
        self.salary.set_attribute(key, value)
        return True

    def published_time_formatter(self):
        hour, minute, second = self.published_at.split('T')[1].split('+')[0].split(':')
        year, month, day = self.published_at.split('T')[0].split('-')
        self.date_time_publishing = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        self.published_at = int(year)

    def get_field(self, field: str):
        if field == 'salary':
            return self.salary.average_salary
        return self.__getattribute__(field)


class DataDictionary:
    salary_years: {int, list}
    vacancies_years: {int, int}
    salary_years_by_profession: {int, list}
    vacancies_years_by_profession: {int, int}
    salaries_cities: {str, list}
    vacancy_cities_ratio: {str, float}
    city_vacancies_count: {str, int}

    def __init__(self):
        self.salary_years = {} #a
        self.vacancies_years = {} #b
        self.salary_years_by_profession = {} #c
        self.vacancies_years_by_profession = {} #d
        self.salaries_cities = {} #e
        self.vacancy_cities_ratio = {} #f
        self.city_vacancies_count = {}

    def update_data(self, vacancies: list, profession: str) -> None:
        for vacancy in vacancies:
            self.update_data_by_vacancy(vacancy, profession)

        self.correct_data(vacancies)

    def update_data_by_vacancy(self, vacancy, profession: str):
        self.update_vacancies_count_dict('city_vacancies_count', 'area_name', vacancy)
        self.update_salary_dict('salary_years', 'published_at', vacancy)
        self.update_vacancies_count_dict('vacancies_years', 'published_at', vacancy)
        self.update_salary_dict('salaries_cities', 'area_name', vacancy)
        self.update_vacancies_count_dict('vacancy_cities_ratio', 'area_name', vacancy)
        if vacancy.name.__contains__(profession):
            self.update_salary_dict('salary_years_by_profession', 'published_at', vacancy)
            self.update_vacancies_count_dict('vacancies_years_by_profession', 'published_at', vacancy)

    def update_salary_dict(self, dict_name: str, field: str, vac: Vacancy) -> None:
        dictionary = self.__getattribute__(dict_name)
        key = vac.get_field(field)
        if key not in dictionary.keys():
            dictionary[key] = [vac.salary.average_salary, 1]
        else:
            dictionary[key][0] += vac.salary.average_salary
            dictionary[key][1] += 1

    def update_vacancies_count_dict(self, dict_name: str, field: str, vac: Vacancy) -> None:
        dictionary = self.__getattribute__(dict_name)
        key = vac.get_field(field)
        if key not in dictionary.keys():
            dictionary[key] = 1
        else:
            dictionary[key] += 1

    def correct_data(self, vacancies: list):
        for key, value in self.vacancy_cities_ratio.items():
            self.vacancy_cities_ratio[key] = round(value / len(vacancies), 4)

        buf = dict(sorted(self.salaries_cities.items(), key=lambda x: x[1][1] / x[1][0]))
        self.salaries_cities = self.get_first(buf, vacancies, 10)

        buf = dict(sorted(self.vacancy_cities_ratio.items(), key=lambda x: x[1], reverse=True))
        self.vacancy_cities_ratio = self.get_first(buf, vacancies, 10)

    def get_first(self, dictionary: dict, vacancies: list, amount: int) -> dict:
        count = 0
        res = {}
        for key, value in dictionary.items():
            if count == amount:
                break
            if self.city_vacancies_count[key] >= len(vacancies) // 100:
                res[key] = value
                count += 1
        return res

    def print(self) -> None:
        print_dictionary: {str, dict} = {
            "Динамика уровня зарплат по годам: ": self.salary_years,
            "Динамика количества вакансий по годам: ": self.vacancies_years,
            "Динамика уровня зарплат по годам для выбранной профессии: ": self.salary_years_by_profession,
            "Динамика количества вакансий по годам для выбранной профессии: ": self.vacancies_years_by_profession,
            "Уровень зарплат по городам (в порядке убывания): ": self.salaries_cities,
            "Доля вакансий по городам (в порядке убывания): ": self.vacancy_cities_ratio
        }
        for key, value in print_dictionary.items():
            if len(value) == 0:
                value = {k: 0 for k in self.salary_years.keys()}
            for k, v in value.items():
                if type(v) is list:
                    value[k] = v[0] // v[1]
            print(f"{key}{value}")


class DataSet:
    def csv_reader(file_name: str):
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
                    vacancies_array.append(vacancy)
        if is_empty_file:
            do_exit("Нет данных")
        return vacancies_array


user_input = UserInput()
vacancies_array = DataSet.csv_reader(user_input.file_name)

if len(vacancies_array) == 0:
    do_exit("Ничего не найдено")

data = DataDictionary()
data.update_data(vacancies_array, user_input.profession)
data.print()
