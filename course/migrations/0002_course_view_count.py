# Generated by Django 3.2.8 on 2021-11-01 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
