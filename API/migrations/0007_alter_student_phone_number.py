# Generated by Django 4.2.7 on 2023-11-14 04:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0006_student_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^\\+998\\d{9}$')], verbose_name='Telefon raqami'),
        ),
    ]