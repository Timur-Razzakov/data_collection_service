# Generated by Django 3.2.9 on 2021-12-03 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0005_auto_20211203_1922'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_and_surname', models.CharField(max_length=256, verbose_name='Имя и фамилия')),
                ('user_name', models.CharField(max_length=256, verbose_name='Никнейм')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name='адрес')),
                ('email_address', models.EmailField(max_length=256, verbose_name='почта')),
                ('phone_number', models.CharField(max_length=120, verbose_name='номер телефона')),
                ('password', models.CharField(max_length=256, verbose_name='password')),
                ('repeat_password', models.CharField(max_length=256, verbose_name='repeat-password')),
                ('country_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraping.city')),
                ('name_of_speciality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraping.speciality')),
            ],
        ),
    ]