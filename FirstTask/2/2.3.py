import csv
import re
import math


class Vacancy:
    average_bound = None

    def __init__(self, dictionary: dict):
        self.name = dictionary["name"]
        self.key_skills = dictionary["key_skills"]
        self.is_premium = dictionary["premium"] == "TRUE"
        self.employer_name = dictionary["employer_name"]
        self.salary_from = int(float(dictionary["salary_from"]))
        self.salary_to = int(float(dictionary["salary_to"]))
        self.salary_currency = dictionary["salary_currency"]
        self.area_name = dictionary["area_name"]

        self.average_bound = (self.salary_to + self.salary_from) // 2


def get_average_salary_string(average_salary: int) -> str:
    res = f"{average_salary} "
    if 10 < average_salary % 100 < 20:
        res += "рублей"
    elif average_salary % 10 == 1:
        res += "рубль"
    elif average_salary % 10 == 0 or average_salary % 10 > 4:
        res += "рублей"
    else:
        res += "рубля"
    return res


def is_correct_values(values: [], currency) -> bool:
    if currency != 'RUR':
        return False
    for value in values:
        if not value:
            return False
    return True


def print_vacancies(vacancies: []):
    count = 1
    for vacancy in vacancies:
        if count == 11:
            break
        print(f"    {count}) {vacancy.name} в компании \"{vacancy.employer_name}\" - {get_average_salary_string(vacancy.average_bound)} "
              f"(г. {vacancy.area_name})")
        count += 1
    print()


def refactor_values(row: dict, skills: dict):
    for key in row.keys():
        if key == 'key_skills':
            add_skills(skills, row[key])
        row[key] = re.sub('<.*?>', '', row[key])
        row[key] = row[key].replace("\r\n", ", ").replace("\n", ", ")
        row[key] = ' '.join(row[key].split()).strip()


def add_skills(skills: dict, skills_string: str):
    for skill in skills_string.replace('\r', '').split('\n'):
        if not skill in skills:
            skills[skill] = 0
        skills[skill] += 1


def print_skills(skills: dict):
    print(f"Из {len(skills.keys())} скиллов, самыми популярными являются:")
    count = 1

    for skill in skills.items():
        if count == 11:
            break
        print(f"    {count}) {skill[0]} - упоминается {get_true_amount(skill[1])}")
        count += 1
    print()


def get_true_amount(num: int) -> str:
    res = f"{num} "
    if 10 < num < 20:
        res += "раз"
    elif 1 < num % 10 < 5:
        res += "раза"
    else:
        res += "раз"
    return res


def add_cities(vacancies: [], cities_count_vacancies: dict, cities_amount_salary: dict):
    for vacancy in vacancies:
        if not vacancy.area_name in cities_count_vacancies:
            cities_count_vacancies[vacancy.area_name] = 0
            cities_amount_salary[vacancy.area_name] = 0
        cities_count_vacancies[vacancy.area_name] += 1
        cities_amount_salary[vacancy.area_name] += vacancy.average_bound

    for city in cities_count_vacancies.items():
        if city[1] >= math.floor(len(vacancies) / 100):
            cities_amount_salary[city[0]] = cities_amount_salary[city[0]] // city[1]
        else:
            cities_amount_salary[city[0]] = 0


def print_average_vacancies(cities_count_vacancies: dict, cities_amount_salary: dict):
    print(f"Из {len(cities_count_vacancies)} городов, самые высокие средние ЗП:")
    count = 1
    for city in cities_amount_salary.items():
        if count == 11:
            break
        city_name = city[0]
        average_salary = city[1]
        count_vacancies = cities_count_vacancies[city_name]
        print(f"    {count}) {city_name} - средняя зарплата {get_average_salary_string(average_salary)}"
              f" ({get_true_string_vacancy(count_vacancies)})")
        count += 1


def get_true_string_vacancy(num: int) -> str:
    res = f"{num} "
    if 10 < num < 20:
        res += "вакансий"
    elif num % 10 == 1:
        res += "вакансия"
    elif 1 < num % 10 < 5:
        res += "вакансии"
    else:
        res += "вакансий"
    return res


file_name = input()
vacancies = []
skills = dict()
cities_count_vacancies = dict()
cities_amount_salary = dict()

with open(file_name, 'r', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if is_correct_values(row.values(), row['salary_currency']):
            refactor_values(row, skills)
            vacancies.append(Vacancy(row))

print("Самые высокие зарплаты:")
print_vacancies(sorted(vacancies, key=lambda vacancy: -vacancy.average_bound))

print("Самые низкие зарплаты:")
print_vacancies(sorted(vacancies, key=lambda vacancy: vacancy.average_bound))

print_skills(dict(sorted(skills.items(), key=lambda item: item[1], reverse=True)))

add_cities(vacancies, cities_count_vacancies, cities_amount_salary)
print_average_vacancies(cities_count_vacancies,
                        dict(sorted(cities_amount_salary.items(), key=lambda item: item[1], reverse=True)))
