# Generated by Django 3.2.4 on 2021-06-11 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='visitor',
            field=models.IntegerField(default=0, verbose_name='访问量'),
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_time',
            field=models.DateTimeField(auto_now=True, verbose_name='创建日期'),
        ),
    ]
