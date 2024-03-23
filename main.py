from src.utils.user_intaraction import UserInteraction, StopUserProgram, COMPANIES
import asyncio

def main():
    print('Приветствую тебя странник')
    
    while True:
        print('Ищешь вакансии компаний?')
        UserInteraction.user_notification_choise()
        while True:
            if not input():
                break
            else:
                print('Напиши через запятую(",") интересующие тебя компании')
                print(f'Если пропустишь то выберется стандартный набор компаний {COMPANIES}')
                companies = input()
                if companies:
                    companies = companies.split(',')
                else: companies = COMPANIES
                asyncio.run(UserInteraction.get_vacancies(companies=companies))
                
        print('Какую професcию ты ищешь?')
        prof = input()
        if not prof:
            print('Неоходимо выбрать профеcсию!')
            continue
        
        print('\nВ каком то конкретом городе?')
        print('Если нет нажми Enter')
        town = input()
        if not town:
            town = None
            
        while True:
            print('\nCколько вакансий тебе требуется?')
            print('Выведется топ по зарплатам\n')
            vacancies = input()
            if not UserInteraction.validate_int(vacancies):
                continue
            
            print('\nКакая страница каталога?\n')
            page = input()
            if not UserInteraction.validate_int(page):
                continue
            
            print('\nХочешь конвертировать иностранную валюту в рубли?\n')
            UserInteraction.user_notification_choise()
            convert = input()
            if not convert:
                convert = False
            else:
                convert = True
            
            print('\nПриступаю к обработке информации')
            
            try:
                UserInteraction.save_to_file(name=prof, page=page, per_page=vacancies, convert_to_RUB=convert, town=town)
                
            except StopUserProgram:
                break
            
                
            print('\nЖелаешь повторить поиск?')
            print('Возможно хочешь выбрать другую страницу либо изменить количество вакансий')
            UserInteraction.user_notification_choise()
            
            if not input():
                break
            continue
        
        print('\nЖелаешь выбрать другую проффесию?')
        print('Либо другой регион?')
        UserInteraction.user_notification_choise()
        
        if not input():
            print('\nДо встречи странник! Да прибудет с тобой Таллос!')
            break
        continue

if __name__ == '__main__':
    main()
    