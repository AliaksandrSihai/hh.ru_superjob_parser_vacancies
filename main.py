import requests

from classes.hh.get_info_from_hh import VacancyHH
from functions.function import user_interaction


def df():
     id_vacancy_x = input()
     id_vacancy_y = None
     sd = [
          {
               "id вакансии:": "83664059",
               "Название вакансии:": "Junior программист/разработчик Frontend backend/Junior разработчик",
               "Дата публикации:": "07-19-2023",
               "https cсылка:": "https://api.hh.ru/vacancies/83664059?host=hh.ru",
               "Заработная плата:": "Не указано",
               "Город:": "Москва",
               "Требование:": "Увлечение микроэлектроникой, мы работаем с ARM, esp32 и т.д. Знание Linux, <highlighttext>Python</highlighttext>, C++. Работа в Git. ",
               "Обязанности:": "Разрабатываем и дорабатываем несколько приложений на Java/kotlin под android. Пишем плагины, много работаем с opensource (нужно уметь читать чужой..."
          },
          {
               "id вакансии:": "83664043",
               "Название вакансии:": "Junior программист/разработчик Frontend backend/Junior разработчик",
               "Дата публикации:": "07-19-2023",
               "https cсылка:": "https://api.hh.ru/vacancies/83664059?host=hh.ru",
               "Заработная плата:": "100000-150000",
               "Город:": "Москва",
               "Требование:": "Увлечение микроэлектроникой, мы работаем с ARM, esp32 и т.д. Знание Linux, <highlighttext>Python</highlighttext>, C++. Работа в Git. ",
               "Обязанности:": "Разрабатываем и дорабатываем несколько приложений на Java/kotlin под android. Пишем плагины, много работаем с opensource (нужно уметь читать чужой..."
          },
          {
               "id вакансии:": "83664023",
               "Название вакансии:": "Junior программист/разработчик Frontend backend/Junior разработчик",
               "Дата публикации:": "07-19-2023",
               "https cсылка:": "https://api.hh.ru/vacancies/83664059?host=hh.ru",
               "Заработная плата:": "100000",
               "Город:": "Москва",
               "Требование:": "Увлечение микроэлектроникой, мы работаем с ARM, esp32 и т.д. Знание Linux, <highlighttext>Python</highlighttext>, C++. Работа в Git. ",
               "Обязанности:": "Разрабатываем и дорабатываем несколько приложений на Java/kotlin под android. Пишем плагины, много работаем с opensource (нужно уметь читать чужой..."
          }
     ]
     salary = ["Не указано", "Не указано"]
     for x in sd:
          if x['id вакансии:'] == id_vacancy_x and id_vacancy_y is None:
               for key, value in x.items():
                    print(key, value)
          elif id_vacancy_y is not None:
               if x['id вакансии:'] == id_vacancy_x or x['id вакансии:'] == id_vacancy_y:
                    salary.append(x["Заработная плата:"])
     return salary


if __name__ == "__main__":
    user_interaction()
    # df()

