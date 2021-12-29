"""
скрипт для запуска скриптов вне проекта
"""

# -*- coding: utf-8 -*-
import json
import os
import sys
import django
from django.contrib.auth import get_user_model
#  you have to set the correct path to you settings module
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
django.setup()

"""модули обязательно должны быть прописаны после 'django.setup()'"""
from scraping.all_parsers.remote_job import main_scraping_part
from scraping.all_parsers.hh_ru import get_data
from scraping.models import Vacancies, City, Speciality, Error

# TODO:написать код, который получает от пользователя city and speciality Done
# TODO:узнать как получить из query_set нужные данные Done
# TODO: написать запуск всех скриптов --Done
# TODO: Понять как заполнить БД полученными данными Done
# Возвращает пользователя по умолчанию
User = get_user_model()

"""
Функция для получения всех городов и специальностей от пользователя
"""

# def get_info_from_user():
#     query_set = User.objects.filter(send_email=True)
#
#
# get_info_from_user()


scrapers = (get_data,)
get_all_cities = City.objects.all()
city = list(get_all_cities.values_list("country_name", flat=True))
get_all_speciality = Speciality.objects.all()
speciality = list(get_all_speciality.values_list("name_of_specialty", flat=True))
print(city, '\n', speciality)

results, errors = [], []
# Запуск скрейперов
for func in scrapers:
    job, error = func(1, city[2], speciality[1])
    results += job
    errors += error
# Заполняем БД данными полученные со скрайперов
for vacancy in results:
    """Удаляем city and speciality из скрипта и передаём их в формате инстанс"""
    city_txt = vacancy.pop("city")
    speciality_txt = vacancy.pop("speciality")
    try:
        country = City(country_name=city_txt).save()
    except Exception:
        country = City.objects.filter(country_name=city_txt).first()
    try:
        prof = Speciality(name_of_specialty=speciality_txt).save()
    except Exception:
        prof = Speciality.objects.filter(name_of_specialty=speciality_txt).first()
    job = Vacancies(**vacancy, city=country, speciality=prof)
    try:
        job.save()
    except Exception as e:
        print(e)
    if errors:
        err = Error(data=errors).save()

# # if __name__ == '__main__':
# #     print(run())
