# Generated by Django 4.2.3 on 2023-07-24 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('slug', models.CharField(blank=True, max_length=150, null=True, verbose_name='slug')),
                ('text', models.TextField(verbose_name='text')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blogs_images/', verbose_name='preview')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('is_published', models.BooleanField(default=True, verbose_name='was published')),
                ('counter_view', models.IntegerField(default=0, verbose_name='counter of views')),
            ],
            options={
                'verbose_name': 'blog',
                'verbose_name_plural': 'blogs',
                'ordering': ('date_created',),
            },
        ),
    ]
