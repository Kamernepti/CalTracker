# Generated by Django 3.1.3 on 2021-01-26 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0002_auto_20210123_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]