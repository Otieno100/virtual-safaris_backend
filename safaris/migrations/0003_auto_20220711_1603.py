# Generated by Django 3.2.7 on 2022-07-11 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safaris', '0002_auto_20220711_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='safaris',
            name='Tourguide',
        ),
        migrations.RemoveField(
            model_name='tourguide',
            name='Safaris',
        ),
        migrations.AlterField(
            model_name='payment',
            name='contact',
            field=models.PositiveIntegerField(default=254799735661, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='contact',
            field=models.PositiveIntegerField(default=254799735661, unique=True),
        ),
        migrations.AlterField(
            model_name='tourguide',
            name='contact',
            field=models.PositiveIntegerField(default=254799735661, unique=True),
        ),
        migrations.AlterField(
            model_name='tourist',
            name='contact',
            field=models.PositiveIntegerField(default=254799735661, unique=True),
        ),
    ]
