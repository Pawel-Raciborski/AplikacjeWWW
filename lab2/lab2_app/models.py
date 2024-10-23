from django.db import models
from django.db.models.functions import Now

# Create your models here.
MONTHS = models.IntegerChoices('Miesiace',
                               'Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień')

SHIRT_SIZES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
)

GENDER = (
    ('M', 'Mężczyzna'),
    ('K', 'Kobieta'),
    ('INNE', 'Inne'),
)


class Gender(models.IntegerChoices):
    INNE = 0
    MEZCZYZNA = 1
    KOBIETA = 2


class Team(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name}"


class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=32, blank=False, null=False)
    opis = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nazwa


class Osoba(models.Model):
    imie = models.CharField(max_length=64, blank=False, null=False)
    nazwisko = models.CharField(max_length=128, blank=False, null=False)
    plec = models.IntegerField(choices=Gender.choices)
    stanowisko = models.ForeignKey(Stanowisko, null=True, on_delete=models.SET_NULL)
    data_dodania = models.DateField(db_default=Now())

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'

    class Meta:
        ordering = ['nazwisko']

class Person(models.Model):
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=64, null=True, blank=True)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    month_added = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}, {self.surname}'
