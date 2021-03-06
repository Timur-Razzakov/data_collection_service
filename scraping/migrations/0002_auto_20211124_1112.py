# Generated by Django 3.2.9 on 2021-11-24 11:12

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('data', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.RenameField(
            model_name='vacancies',
            old_name='specialty',
            new_name='speciality',
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.city', verbose_name='Город')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.speciality', verbose_name='Язык программирования')),
            ],
            options={
                'unique_together': {('city', 'speciality')},
            },
        ),
    ]
