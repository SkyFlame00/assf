# Generated by Django 2.0.3 on 2018-05-10 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180510_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='university',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
