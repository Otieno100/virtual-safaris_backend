# Generated by Django 4.0.6 on 2022-07-08 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safaris', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(default=2, max_length=30),
            preserve_default=False,
        ),
    ]
