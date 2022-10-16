import math

class Worker:
    average_bound = None
    def __init__(self, vacansy: str, description_vacansy: str, expirience: int,
                 lower_bound: int, higher_bound: int,
                 is_free_shedul: bool, is_premium_vacansy: bool):
        self.vacansy = vacansy
        self.description_vacansy = description_vacansy
        self.expirience = expirience
        self.lower_bound = lower_bound
        self.higher_bound = higher_bound
        self.is_free_shedul = is_free_shedul
        self.is_premium_vacansy = is_premium_vacansy
        self.average_bound = 0
        count = 0
        for i in range(self.lower_bound, self.higher_bound + 1):
            count += 1
            self.average_bound += i
        self.average_bound = math.floor(self.average_bound / count)


    def expirience_to_string(self):
        print(f"Требуемый опыт работы: {self.expirience} ", end="")
        if (self.expirience > 10 and self.expirience < 20):
            print("лет")
        elif (self.expirience % 10 == 1):
            print("год")
        elif (self.expirience % 10 == 0 or self.expirience % 10 > 4):
            print("лет")
        else:
            print("года")

    def average_bound_to_string(self):
        print(f"Средний оклад: {self.average_bound} ", end="")
        if (self.average_bound> 10 and self.average_bound < 20):
            print("рублей")
        elif(self.average_bound % 10 == 1):
            print("рубль")
        elif (self.average_bound % 10 == 0 or self.average_bound % 10 > 4):
            print("рублей")
        else:
            print("рубля")

    def to_string(self):
        print(f"{self.vacansy}")
        print(f"Описание: {self.description_vacansy}")
        self.expirience_to_string()
        self.average_bound_to_string()
        print(f"Свободный график: {'да' if self.is_free_shedul else 'нет'}")
        print(f"Премиум-вакансия: {'да' if self.is_premium_vacansy else 'нет'}")

vacansy = input("Введите название вакансии: ")
description_vacansy = input("Введите описание вакансии: ")
work_expirience = int(input("Введите требуемый опыт работы (лет): "))
lower_bound = int(input("Введите нижнюю границу оклада вакансии: "))
higher_bound = int(input("Введите верхнюю границу оклада вакансии: "))
is_free_shedul = input("Есть ли свободный график (да / нет): ") == "да"
is_premium_vacansy = input("Является ли данная вакансия премиум-вакансией (да / нет): ") == "да"

worker = Worker(vacansy, description_vacansy, work_expirience,
                lower_bound, higher_bound, is_free_shedul, is_premium_vacansy)

worker.to_string()