# Generated by Django 4.2.3 on 2023-08-19 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='used_at',
        ),
    ]
