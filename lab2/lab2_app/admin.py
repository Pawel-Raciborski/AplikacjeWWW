from django.contrib import admin

from lab2_app.models import Osoba
from lab2_app.models import Person
from lab2_app.models import Stanowisko


class OsobaAdmin(admin.ModelAdmin):
    readonly_fields = ['data_dodania']


# Register your models here.
admin.site.register(Person)
admin.site.register(Osoba, OsobaAdmin)
admin.site.register(Stanowisko)
