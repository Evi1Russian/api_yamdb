# Generated by Django 2.2.16 on 2022-08-11 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_auto_20220811_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
