# Generated by Django 3.0.4 on 2020-05-10 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobSite_app', '0003_auto_20200509_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
    ]
