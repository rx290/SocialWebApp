# Generated by Django 3.2 on 2021-05-01 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_auto_20210501_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_time',
            field=models.CharField(default='05-01-2021 11:11:29 AM', max_length=50),
        ),
    ]
