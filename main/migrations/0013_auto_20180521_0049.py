# Generated by Django 2.0.3 on 2018-05-21 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20180521_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='foundation_year',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='competency',
            name='title',
            field=models.CharField(max_length=150),
        ),
    ]
