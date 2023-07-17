import requests
from classes.hh.get_info_from_hh import GetInfo


class SuperJobAPI(GetInfo):
    """Класс и метод для получения вакансий с superjob"""

    def __init__(self, keyword='python'):
        self.keyword = keyword
        self.per_page = None
        self.city = None

    def get_vacancies(self, keyword):
        self.keyword = keyword
        url = '	https://api.superjob.ru/2.0/vacancies/'
        response = requests.get(url, params={
            'app_key': 'v3.r.137674414.848efdee01573fb591d07cadb57a0f1327d39da5.ab04515408443830da7ac08677fa0b5d01821d0d',
            'keyword': self.keyword,
            'count': 1
        })
        rp = response.json()
        return rp


aw = SuperJobAPI()
print(aw.get_vacancies('python'))
