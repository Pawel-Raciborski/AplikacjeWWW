# Generated by Django 5.1.2 on 2024-11-06 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab2_app', '0006_alter_osoba_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osoba',
            name='data_dodania',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
