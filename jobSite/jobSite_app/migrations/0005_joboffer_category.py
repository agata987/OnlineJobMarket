# Generated by Django 3.0.4 on 2020-05-25 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobSite_app', '0004_auto_20200510_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='joboffer',
            name='category',
            field=models.CharField(default='inne', max_length=25),
        ),
    ]
