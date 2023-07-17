import json
import os
from datetime import datetime

from classes.abstract.abstract_class import GetInfo, JSONSaver, InputError

import requests


class HeadHunterAPI(GetInfo):
    """Класс для получения вакансий с hh"""

    def __init__(self):
        """Инициализируемся по слову, которое вводит пользователь"""
        self.keyword = None
        self.per_page = None
        self.info = None

    def get_vacancies(self, keyword: str):
        """Метод в котором получаем вакансии по заданным параметрам"""
        self.keyword = keyword
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': self.keyword
        }
        response = requests.get(url, params=params)
        vacancies = response.json()
        return vacancies


# class SortedListHH(HeadHunterAPI, InputError):
#     """Класс и метод для сортировки вакансии по критериям"""
#
#     def sorted_vacancy(self, per_page, info):
#         data = self.get_vacancies(self.keyword)
#         self.per_page = per_page
#         self.info = info
#         if data:
#             sorted_vacancy = []
#             for item in data['items']:
#                 salary = item['salary']
#                 salary_range = f"{salary['from']}-{salary['to']},
#                 валюта {salary['currency']}" if salary and salary['from'] and salary[
#                     'to'] else "Не указано"
#                 date = item['published_at']
#                 date_str = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
#                 publish_time = date_str.strftime('%m-%d-%Y')
#                 vacancy = {
#                     'id вакансии': item['id'],
#                     'Название вакансии': item['name'],
#                     'Дата публикации': publish_time,
#                     'Заработная плата': salary_range,
#                     'Город': item["area"]["name"],
#                     'Требование': item['snippet']['requirement'],
#                     'Обязанности': item['snippet']['responsibility'],
#                     'https cсылка': item['url']
#                 }
#                 sorted_vacancy.append(vacancy)
#             for x in sorted_vacancy:
#                 if self.info is not None and self.info in x['Город']:
#                     sorted_vacancy = sorted(sorted_vacancy, key=lambda x: x['Город'] == self.info)
#                 else:
#                     sorted_vacancy.sort(key=lambda x: x.get(self.info), reverse=True)
#
#             return sorted_vacancy[:self.per_page]
#         else:
#             raise InputError
#


class WorkWithJsonHH(HeadHunterAPI, JSONSaver):
    file_path = '/home/aliaksandr_sigai/lesson_ООП/Course_work_4/vacancy_from_hh.json'

    def add_vacancy(self, vacancy):
        if os.path.isfile(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
                existing_data.extend(vacancy)
            with open(self.file_path, 'w',
                      encoding='utf-8') as file_add:
                json.dump(existing_data, file_add, ensure_ascii=False, indent=4)
        else:
            with open(self.file_path, 'w', encoding='utf-8') as file_add:
                json.dump(vacancy, file_add, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy_del):
        if os.path.isfile(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for x in data:
                    if x['id вакансии'] == vacancy_del:
                        data.remove(x)
                    else:
                        print("asd")
                with open(self.file_path, 'w', encoding='utf-8') as file_del:
                    json.dump(data, file_del, ensure_ascii=False, indent=4)

    def get_vacancies_by(self, id_vacancy):
        with open('vacancy_from_hh.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for x in data:
                if x['id вакансии'] == id_vacancy:
                    for key, value in x.items():
                        print(key, value)


class Vacancy(WorkWithJsonHH, InputError):
    """Класс для работы с вакансиями"""

    def __init__(self, vacancy_id=None, vacancy_name=None, vacancy_date=None,
                 vacancy_url=None, vacancy_salary=None,
                 vacancy_city=None, vacancy_requirement=None,
                 vacancy_responsibility=None):
        try:
            self.vacancy_id = vacancy_id
            self.vacancy_name = vacancy_name
            self.vacancy_date = vacancy_date
            self.vacancy_url = vacancy_url
            self.vacancy_salary = vacancy_salary
            self.vacancy_city = vacancy_city
            self.vacancy_requirement = vacancy_requirement
            self.vacancy_responsibility = vacancy_responsibility
        except InputError as m:
            print(m.message)

    def sorted_vacancy(self, per_page, info):
        data = self.get_vacancies(self.keyword)
        self.per_page = per_page
        self.info = info
        if data:
            sorted_vacancy = []
            for item in data['items']:
                salary = item['salary']
                salary_range = f"{salary['from']}-{salary['to']}, валюта {salary['currency']}" if salary and salary[
                    'from'] and salary['to'] else "Не указано"
                date = item['published_at']
                date_str = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
                publish_time = date_str.strftime('%m-%d-%Y')
                vacancy = {
                    'id вакансии': item['id'],
                    'Название вакансии': item['name'],
                    'Дата публикации': publish_time,
                    'Заработная плата': salary_range,
                    'Город': item["area"]["name"],
                    'Требование': item['snippet']['requirement'],
                    'Обязанности': item['snippet']['responsibility'],
                    'https cсылка': item['url']
                }
                sorted_vacancy.append(vacancy)
            for x in sorted_vacancy:
                if self.info is not None and self.info in x['Город']:
                    sorted_vacancy = sorted(sorted_vacancy, key=lambda x: x['Город'] == self.info)
                else:
                    sorted_vacancy.sort(key=lambda x: x.get(self.info), reverse=True)

            return sorted_vacancy[:self.per_page]
        else:
            raise InputError

    def to_json(self):
        """Преобразование объекта Vacancy в словарь"""
        return {
            'id вакансии:': self.vacancy_id,
            'Название вакансии:': self.vacancy_name,
            'Дата публикации:': self.vacancy_date,
            'https cсылка:': self.vacancy_url,
            'Заработная плата:': self.vacancy_salary,
            'Город:': self.vacancy_city,
            'Требование:': self.vacancy_requirement,
            'Обязанности:': self.vacancy_responsibility
        }

    def __le__(self, other):
        """Магический метод для проверки зп <="""
        try:
            salary_self = int(self.vacancy_salary)
            salary_other = int(other.vacancy_salary)
            if salary_self <= salary_other:
                return True
            else:
                raise ValueError
        except ValueError:
            if self.vacancy_salary == "Не указано":
                return (f"Вакансия: {other.vacancy_name}\n"
                        f"Зарплата: {other.vacancy_salary}\n"
                        f"Ссылка на вакансию: {self.vacancy_url}\n")
            elif other.vacancy_salary == "Не указано":
                return (f"Вакансия: {other.vacancy_name}\n"
                        f"Зарплата: {self.vacancy_salary}\n"
                        f"Ссылка на вакансию: {self.vacancy_url}\n")

    def __ge__(self, other):
        """Магический метод для проверки зп >="""
        try:
            salary_self = int(self.vacancy_salary)
            salary_other = int(other.vacancy_salary)
            if salary_self >= salary_other:
                return True
            else:
                raise ValueError
        except ValueError:
            if self.vacancy_salary == "Не указано":
                return (f"Вакансия: {other.vacancy_name}\n"
                        f"Заработная плата: {other.vacancy_salary}\n"
                        f"Ссылка на вакансию: {self.vacancy_url}\n")
            elif other.vacancy_salary == "Не указано":
                return (f"Вакансия: {other.vacancy_name}\n"
                        f"Заработная плата: {self.vacancy_salary}\n"
                        f"Ссылка на вакансию: {self.vacancy_url}\n")
