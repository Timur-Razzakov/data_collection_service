# Generated by Django 3.2.9 on 2021-11-27 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_auto_20211124_1112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='error',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='error',
            name='data',
            field=models.JSONField(),
        ),
    ]
