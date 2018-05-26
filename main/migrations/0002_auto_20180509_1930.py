# Generated by Django 2.0.3 on 2018-05-09 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='universityprogram',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='universityprogram',
            name='competencies',
            field=models.ManyToManyField(default=None, null=True, to='main.Competency'),
        ),
    ]
