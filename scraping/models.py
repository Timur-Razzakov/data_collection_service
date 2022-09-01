from django.db import models


class City(models.Model):
    country_name = models.CharField(unique=True,
                                    max_length=255,
                                    verbose_name='Название города')
    slug = models.SlugField(unique=True,
                            blank=True,
                            max_length=60)

    def __str__(self):
        return self.country_name


class Speciality(models.Model):
    name_of_specialty = models.CharField(unique=True,
                                        max_length=255,
                                        verbose_name='Наименование специальности')
    slug = models.SlugField(unique=True, blank=True, max_length=60)

    def __str__(self):
        return self.name_of_specialty


class Vacancies(models.Model):
    url = models.URLField(unique=True, verbose_name="Ссылка на вакансию")
    title = models.CharField(max_length=255, verbose_name='Заголовок вакансии')
    description = models.TextField(verbose_name='Описание вакансии')
    company_name = models.CharField(max_length=255, verbose_name='Наименовании компании')
    salary = models.CharField(max_length=255, blank=True, verbose_name='Заработная плата', default=None)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE, blank=True)
    speciality = models.ForeignKey(Speciality,
                                verbose_name='Специальность',
                                on_delete=models.CASCADE,
                                blank=True)
    created_at = models.DateField(verbose_name='Дата публикации')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Error(models.Model):
    created_at = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.created_at)
