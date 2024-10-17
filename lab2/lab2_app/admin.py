from django.contrib import admin

from lab2_app.models import Person
from lab2_app.models import Osoba
from lab2_app.models import Stanowisko

# Register your models here.
admin.site.register(Person)
admin.site.register(Osoba)
admin.site.register(Stanowisko)