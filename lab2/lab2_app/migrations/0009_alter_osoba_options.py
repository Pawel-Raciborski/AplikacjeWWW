# Generated by Django 5.1.2 on 2024-11-20 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2_app', '0008_osoba_wlasciciel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='osoba',
            options={'ordering': ['nazwisko'], 'permissions': [('can_view_other_persons', 'Can view other persons')]},
        ),
    ]