# Generated by Django 2.2.16 on 2022-08-11 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrator'), ('moderator', 'Moderator'), ('user', 'User')], default='user', max_length=20, verbose_name='Роль'),
        ),
    ]
