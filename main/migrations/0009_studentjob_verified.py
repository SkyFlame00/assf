# Generated by Django 2.0.5 on 2018-05-12 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_studenteducation_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentjob',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
