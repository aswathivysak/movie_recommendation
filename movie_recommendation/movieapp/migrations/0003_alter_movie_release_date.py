# Generated by Django 5.0.3 on 2024-03-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0002_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='Release_date',
            field=models.DateField(),
        ),
    ]
