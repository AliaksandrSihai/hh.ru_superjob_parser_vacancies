import json
from abc import ABC, abstractmethod

class GetInfo(ABC):
    """Абстрактный класс с объявлением метода для получения информации"""

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class SaveJson(ABC):
    def save_to_json(self, data, json_name):
        with open(json_name, 'w') as file:
            file.write(json.dumps(data))

    @abstractmethod
    def save_vacancies_to_json(self, data=None, json_name=None):
        pass
