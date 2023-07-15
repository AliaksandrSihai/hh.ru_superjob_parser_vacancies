import json
from abc import ABC, abstractmethod

class GetInfo(ABC):
    """Абстрактный класс и метода для получения информации через API"""

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class JSONSaver(ABC):
    def save_to_json(self, data, json_name):
        with open(json_name, 'w') as file:
            file.write(json.dumps(data))

    @abstractmethod
    def save_vacancies_to_json(self, data=None, json_name=None):
        pass

    def add_vacancy(self, vacancy):
        pass

    def get_vacancies_by_salary(self, salary:str):
        pass

    def delete_vacancy(self, vacancy):
        pass

class InputError(Exception):
    def __init__(self):
        self.message = "Ошибка ввода данных"
