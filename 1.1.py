def print_type(a):
    print(f"{a} (", end="")
    if(isinstance(a, str)):
        print("str)")
    elif (isinstance(a, bool)):
        print("bool)")
    elif(isinstance(a, int)):
        print("int)")

vacansy = input("Введите название вакансии: ")
description_vacansy = input("Введите описание вакансии: ")
work_expirience = int(input("Введите требуемый опыт работы (лет): "))
lower_bound = int(input("Введите нижнюю границу оклада вакансии: "))
higher_bound = int(input("Введите верхнюю границу оклада вакансии: "))
is_free_shedul = input("Есть ли свободный график (да / нет): ") == "да"
is_premium_vacansy = input("Является ли данная вакансия премиум-вакансией (да / нет): ") == "да"

description_work = [vacansy, description_vacansy, work_expirience,
                    lower_bound, higher_bound, is_free_shedul, is_premium_vacansy]

for i in description_work:
    print_type(i)