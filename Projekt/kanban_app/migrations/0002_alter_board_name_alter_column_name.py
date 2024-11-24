# Generated by Django 5.1.2 on 2024-11-24 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='column',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
