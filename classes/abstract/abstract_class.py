import json
import os
from abc import ABC, abstractmethod


class GetInfo(ABC):
    """Абстрактный класс и метода для получения информации через API"""

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class JSONSaver(ABC):
    @staticmethod
    def save_to_json(data, json_name):
        with open(json_name, 'w') as file:
            file.write(json.dumps(data))

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by(self, salary: str):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class InputError(Exception):
    def __init__(self):
        self.message = "Ошибка ввода данных"


class WorkWithJson(JSONSaver):
    """Класс для работы с json файлом"""

    file_path = '/home/aliaksandr_sigai/lesson_ООП/Course_work_4/vacancy_from.json'

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
        if os.path.isfile(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'r', encoding='utf-8') as file:
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
