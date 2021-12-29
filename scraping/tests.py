from django.test import TestCase

# Create your tests here.
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
from icecream import ic

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
""" Все скрейперы """
scrapers = (get_data, main_scraping_part)


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['speciality_id']) for q in qs)
    return settings_lst


print(get_settings())


def get_data(_settings):
    qs = Vacancies.objects.all().values()
    general_dct = {(q['city_id'], q['speciality_id']) for q in qs}
    ic(general_dct)
    speciality_city_list = []
    for pair in _settings:
        if pair in general_dct:
            tmp = {}
            tmp['city'] = City.objects.filter(id=pair[0]).first().country_name
            tmp['speciality'] = Speciality.objects.filter(id=pair[1]).first().name_of_specialty
            speciality_city_list.append(tmp)
    return speciality_city_list


settings = get_settings()
data_list = get_data(settings, )
print(data_list.city)

results, errors = [], []
# Запуск скрейперов
for func in scrapers:
    job, error = func(1, )
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
