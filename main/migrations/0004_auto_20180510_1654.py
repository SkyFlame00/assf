# Generated by Django 2.0.3 on 2018-05-10 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_company_studenteducation_studentjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='foundation_year',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]