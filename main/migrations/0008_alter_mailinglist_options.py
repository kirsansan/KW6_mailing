# Generated by Django 4.2.3 on 2023-08-22 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_client_options_alter_mailinglist_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailinglist',
            options={'get_latest_by': 'time', 'permissions': [('change_active', 'Can change active flag')], 'verbose_name': 'mailing list', 'verbose_name_plural': 'mailing lists'},
        ),
    ]
