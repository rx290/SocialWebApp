# Generated by Django 3.1.2 on 2021-05-01 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0002_auto_20210501_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.CharField(default='05/01/2021 07:08:34 AM', max_length=50),
        ),
    ]
