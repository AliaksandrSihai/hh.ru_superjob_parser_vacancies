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
        self.city = None

    def get_vacancies(self, keyword: str, city=None):
        """Метод в котором получаем вакансии по заданным параметрам"""
        self.city = city
        self.keyword = keyword
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': self.keyword
        }
        response = requests.get(url, params=params)
        vacancies = response.json()
        return vacancies


class WorkWithJsonHH(HeadHunterAPI, JSONSaver):
    """Класс для работы с json файлом"""
    file_path = '/home/aliaksandr_sigai/lesson_ООП/Course_work_4/vacancy_from_hh.json'

    def add_file(self, data: list):
        with open(self.file_path, 'w', encoding='utf-8') as file_add:
            json.dump(data, file_add, ensure_ascii=False, indent=4)

    def add_vacancy(self, id_vacancy):
        """Метод добавления по id в json файл """
        if os.path.isfile(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
                existing_data.extend(id_vacancy)
            with open(self.file_path, 'r+',
                      encoding='utf-8') as file_add:
                json.dump(existing_data, file_add, ensure_ascii=False, indent=4)
                return
        else:
            with open(self.file_path, 'w', encoding='utf-8') as file_add:
                json.dump(id_vacancy, file_add, ensure_ascii=False, indent=4)
                return

    def delete_vacancy(self, id_vacancy):
        """Метод удаления по id в json файл """
        if os.path.isfile(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for x in data:
                    if x['id вакансии:'] == id_vacancy:
                        data.remove(x)
                    else:
                        print(f"Вакансия с id {id_vacancy} не найдена в файле.")
                with open(self.file_path, 'w', encoding='utf-8') as file_del:
                    json.dump(data, file_del, ensure_ascii=False, indent=4)
                    return

    def get_vacancies_by(self, id_vacancy_x, id_vacancy_y=None):
        """Получение всей информации о вакансии по её id"""
        with open('vacancy_from_hh.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            salary = []
            for x in data:
                if x['id вакансии:'] == id_vacancy_x and id_vacancy_y is None:
                    for key, value in x.items():
                        print(key, value)
                elif id_vacancy_y is not None:
                    if x['id вакансии:'] == id_vacancy_x or x['id вакансии:'] == id_vacancy_y:
                        salary.append(x["Заработная плата:"])
            return salary


class VacancyHH(WorkWithJsonHH, InputError):
    """Класс для работы с вакансиями"""

    def __init__(self, vacancy_id=None, vacancy_name=None, vacancy_date=None,
                 vacancy_url=None, vacancy_salary=None,
                 vacancy_city=None, vacancy_requirement=None,
                 vacancy_responsibility=None):
        """Инициализация по параметрам  """
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

    def sorted_vacancy(self):
        """Метод сортировки информации из api hh в универсальный """
        data = self.get_vacancies(self.keyword)
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
        return sorted_vacancy

    def sort_by(self, info, per_page):

        self.per_page = per_page
        self.info = info
        sorted_vacancy = self.sorted_vacancy()
        if sorted_vacancy:
            sorted_by_city = []
            for x in sorted_vacancy:
                if self.info is not None and self.info in x['Город']:
                    sorted_by_city.append(x)
                else:
                    sorted_vacancy.sort(key=lambda x: x.get(self.info, ''), reverse=True)
            if len(sorted_by_city) > 0:
                for x in sorted_by_city:
                    sorted_by_city.sort(key=lambda x: x.get('Дата публикации', ''), reverse=True)
                return sorted_by_city[:self.per_page]
            else:
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
                        f"Заработная плата: {other.vacancy_salary}\n"
                        f"Ссылка на вакансию: {self.vacancy_url}\n")
            elif other.vacancy_salary == "Не указано":
                return (f"Вакансия: {other.vacancy_name}\n"
                        f"Заработная плата: {self.vacancy_salary}\n"
                        f"Ссылка на вакансию: {self.vacancy_url}\n")

    def __ge__(self, other):
        """Магический метод для проверки зп >="""
        try:
            salary_other = int(other.vacancy_salary)
            if self.vacancy_salary >= salary_other:
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
