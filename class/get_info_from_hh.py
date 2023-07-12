import json
from abstract_class import GetInfo, SaveJson

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
            "per_page": 2
        }
        response = requests.get(url, params=params)
        vacancies = response.json()
        return vacancies


class SortedListHH(HeadHunterAPI, SaveJson):
    def save_vacancies_to_json(self, data=None, json_name=None):
        data = self.get_vacancies(self.keyword)
        json_name = 'vacancy_from_hh.json'
        with open(json_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def sorted_vacancy(self):
        with open('vacancy_from_hh.json', 'r') as file:
            data = json.load(file)
            sorted_vacancy = []
            for item in data['items']:
                vacancy = {
                    'id вакансии': item['id'],
                    'Название вакансии': item['name'],
                    'Заработная плата': item['salary'],
                    'Ссылка на вакансию': item['url'],
                    'Требование': item['snippet']['requirement'],
                    'Обязанности': item['snippet']['responsibility'],
                    'Адресс': item['address']['raw']
                }
                sorted_vacancy.append(vacancy)
        return sorted_vacancy


df = SortedListHH()
df.get_vacancies('python')
df.save_vacancies_to_json()
print(df.sorted_vacancy())
