# Generated by Django 5.0.3 on 2024-03-22 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0004_reviewrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='slug',
        ),
    ]