# Generated by Django 3.0.3 on 2020-02-07 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200207_1042'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]