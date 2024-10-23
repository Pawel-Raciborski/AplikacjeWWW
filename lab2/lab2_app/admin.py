from django.contrib import admin

from lab2_app.models import Osoba
from lab2_app.models import Person
from lab2_app.models import Stanowisko


class OsobaAdmin(admin.ModelAdmin):
    readonly_fields = ['data_dodania']
    list_display = ['imie', 'nazwisko', 'plec','display_stanowisko','data_dodania']
    list_filter = ['data_dodania','stanowisko']

    @admin.display(description="Stanowisko")
    def display_stanowisko(self,obj):
        return f'{obj.stanowisko} ({obj.stanowisko_id})'


# Register your models here.
admin.site.register(Person)
admin.site.register(Osoba, OsobaAdmin)
admin.site.register(Stanowisko)
