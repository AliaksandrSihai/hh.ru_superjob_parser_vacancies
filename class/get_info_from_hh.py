import html
import json
from abstract_class import GetInfo, JSONSaver, InputError

import requests


class HeadHunterAPI(GetInfo):
    """Класс для получения вакансий с hh"""

    def __init__(self, keyword='python'):
        self.keyword = keyword
        self.per_page = None
        self.city = None

    def get_vacancies(self, keyword: str):
        """Метод в котором получаем вакансии по заданным параметрам"""
        self.keyword = keyword
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': self.keyword,
            "per_page": 5
        }
        response = requests.get(url, params=params)
        vacancies = response.json()
        return vacancies

class SortedListHH(HeadHunterAPI, InputError):
    def save_vacancies_to_json(self, data=None, json_name=None):
        data = self.get_vacancies(self.keyword)
        json_name = 'vacancy_from_hh.json'
        with open(json_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def sorted_vacancy(self):
            data = self.get_vacancies(self.keyword)
            if data:
                sorted_vacancy = []
                for item in data['items']:
                    salary = item['salary']
                    salary_range = f"{salary['from']}-{salary['to']}"if salary and salary['from'] and salary['to'] else "Не указано"
                    vacancy = {
                        'id вакансии': item['id'],
                        'Название вакансии': item['name'],
                        'Заработная плата': salary_range,
                        'https cсылка  вакансии': item['url'],
                        'Требование': item['snippet']['requirement'],
                        'Обязанности': item['snippet']['responsibility'],
                        'Город': item["area"]["name"]
                    }
                    sorted_vacancy.append(vacancy)
                return sorted_vacancy
            else:
                raise InputError


    def get_get_vacancies_by(self, *args, **kwargs):
        # salary_start = salary
        # with open('vacancy_from_hh.json', 'r', encoding='utf-8') as file:
        # vacancy = json.load(file)
        vacancy = self.sorted_vacancy()
        for x in vacancy:
            salary = x['Заработная плата']
            print(salary)

class Vacancy(SortedListHH):
    def __init__(self, keyword, vacancy_name,  vacancy_salary, vacancy_url, vacancy_city, vacancy_requirements ):
        super().__init__(keyword)
        try:
            self.vacancy_name  = vacancy_name
            self.vacancy_salary = vacancy_salary
            self.vacancy_url  = vacancy_url
            self.vacancy_city  = vacancy_city
            self.vacancy_requirements = vacancy_requirements
        except InputError as m:
            print(m.message)

    def __le__(self, other):
        return self.vacancy_salary <= other.vavacancy_salary

    def __ge__(self, other):
        return self.vacancy_salary >= other.vavacancy_salary




class   SaveToJsonHH(SortedListHH, JSONSaver):
    def save_vacancies_to_json(self, data=None, json_name=None):
        data = self.sorted_vacancy()
        json_name = 'vacancy_from_hh.json'
        with open(json_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        with open('vacancy_from_hh.json', 'w', encoding='utf-8') as file:
            json.dump(vacancy, file, ensure_ascii=False, indent=4)

    def get_vacancies_by_salary(self, salary:str):
        with open('vacancy_from_hh.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for x in data:
                if x["Заработная плата"] == salary:
                    print (x)


    def delete_vacancy(self, vacancy_del):
        with open('vacancy_from_hh.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            updated_data = [d for d in data if d["id вакансии"] != vacancy_del]
            with open('vacancy_from_hh.json', 'w') as file:
                json.dump(updated_data, file, ensure_ascii=False, indent=4)

df = SortedListHH()
df.get_vacancies('python')
#df.save_vacancies_to_json()
#print(df.get_get_vacancies_by_salary())
#print(df.sorted_vacancy())
ds = SaveToJsonHH()

#sd = Vacancy()
ds.add_vacancy(df.sorted_vacancy())
ds.get_vacancies_by_salary("40000-80000")