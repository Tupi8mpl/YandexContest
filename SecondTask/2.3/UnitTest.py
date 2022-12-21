from datetime import datetime
from Testing import UserInput, Salary, Vacancy
from unittest import TestCase


class UserInputTests(TestCase):
    def test_user_input_type(self):
        self.assertEqual(type(UserInput()).__name__, 'UserInput')

    def test_user_input_default_file_name(self):
        self.assertEqual(UserInput().file_name, 'vacancies_by_year.csv')

    def test_user_input_file_name(self):
        self.assertEqual(UserInput(file_name='vacancies.csv').file_name, 'vacancies.csv')

    def test_user_input_default_profession(self):
        self.assertEqual(UserInput().profession, 'Аналитик')

    def test_user_input_profession(self):
        self.assertEqual(UserInput(profession='Программист').profession, 'Программист')


class SalaryTests(TestCase):
    def test_salary_type(self):
        self.assertEqual(type(Salary()).__name__, 'Salary')

    def test_salary_from(self):
        self.assertEqual(Salary(5, 10, 'EUR').salary_from, 5)

    def test_salary_to(self):
        self.assertEqual(Salary(5, 10, 'EUR').salary_to, 10)

    def test_salary_currency(self):
        self.assertEqual(Salary(5, 10, 'EUR').salary_currency, 'EUR')

    def test_salary_average(self):
        self.assertEqual(Salary(5, 10, 'EUR').average_salary, 7)

    def test_average_salary_rur(self):
        self.assertEqual(Salary(5, 10, 'EUR').average_salary_rur, 449)


class VacancyTests(TestCase):
    def test_vacancy_type(self):
        self.assertEqual(type(Vacancy({})).__name__, 'Vacancy')

    def test_vacancy_name(self):
        self.assertEqual(Vacancy({'name': 'Аналитик'}).name, 'Аналитик')

    def test_vacancy_employer(self):
        self.assertEqual(Vacancy({'employer_name': 'Компания'}).employer_name, 'Компания')

    def test_vacancy_salary_from(self):
        self.assertEqual(Vacancy({'salary_from': 100}).salary.salary_from, 100)

    def test_vacancy_salary_average(self):
        self.assertEqual(Vacancy({'salary_from': '5',
                                  'salary_to': '10',
                                  'salary_currency': 'EUR'}).salary.average_salary, 7)

    def test_vacancy_area(self):
        self.assertEqual(Vacancy({'area_name': "Екатеринбург"}).area_name, "Екатеринбург")

    def test_vacancy_published_at(self):
        self.assertEqual(Vacancy({'published_at': '2023-01-01T10:00:00+00'}).published_at, 2023)

    def test_vacancy_date_time_publishing(self):
        self.assertEqual(Vacancy({'published_at': '2023-01-01T10:00:00+00'}).date_time_publishing,
                         datetime(2023, 1, 1, 10, 0))