
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=255, unique=True, verbose_name='Название города')),
                ('slug', models.SlugField(blank=True, max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_specialty', models.CharField(max_length=255, unique=True, verbose_name='Наименование специальности')),
                ('slug', models.SlugField(blank=True, max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True, verbose_name='Ссылка на вакансию')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок вакансии')),
                ('description', models.TextField(verbose_name='Описание вакансии')),
                ('company_name', models.CharField(max_length=255, verbose_name='Наименовании компании')),
                ('salary', models.CharField(blank=True, default=None, max_length=255, verbose_name='Заработная плата')),
                ('created_at', models.DateField(verbose_name='Дата публикации')),
                ('city', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.city', verbose_name='Город')),
                ('speciality', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.speciality', verbose_name='Специальность')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
