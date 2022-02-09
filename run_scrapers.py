"""
скрипт для запуска скриптов вне проекта
"""
import asyncio
import os
import sys
import django
from django.contrib.auth import get_user_model
from icecream import ic

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
django.setup()
# -------------------------------------------------------------------------------
"""модули обязательно должны быть прописаны после 'django.setup()'"""
from scraping.all_parsers.remote_job import main_scraping_part
from scraping.all_parsers.hh_ru import get_data
from scraping.models import Vacancies, City, Speciality, Error

# Возвращает пользователя по умолчанию
User = get_user_model()

""" Все скрейперы """
scrapers = (get_data, main_scraping_part)


# Получение city_id,speciality_id у пользователей, которых стоит галочка на получение писем по почте
def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['speciality_id']) for q in qs)
    ic(settings_lst)
    return settings_lst


# получаем имена городов и специальностей
def getdata(_settings):
    speciality_city_list = []
    for pair in _settings:
        ic(pair)
        tmp = {}
        tmp['city'] = City.objects.filter(id=pair[0]).first().country_name
        tmp['speciality'] = Speciality.objects.filter(id=pair[1]).first().name_of_specialty
        speciality_city_list.append(tmp)

    return speciality_city_list


"""Асинхронный запуск скриптов"""
results, errors = [], []
settings = get_settings()
data_list = getdata(settings)


async def run_scripts(value):
    func, count_page, city, specialty = value
    # run
    job, error = await loop.run_in_executor(None,func, count_page, city, specialty)
    errors.extend(error)
    results.extend(job)

loop = asyncio.get_event_loop()
# задания для асинхронного запуска
tmp_tasks = [(func, 1, data['city'], data['speciality'])
             for data in data_list
             for func in scrapers]
#  создаём указанные задания и вызываем их
tasks = asyncio.wait([loop.create_task(run_scripts(task)) for task in tmp_tasks])
# # Запуск скрейперов
# for data in data_list:
#     for func in scrapers:
#         job, error = func(1, city=data['city'], speciality=data['speciality'])
#         results += job
#         errors += error

# Заполняем БД данными полученные со скрайперов
loop.run_until_complete(tasks)
# закрывем
loop.close()

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

