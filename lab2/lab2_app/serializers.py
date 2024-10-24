from lab2_app.models import Osoba, Stanowisko, Gender
from rest_framework import serializers


class OsobaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    imie = serializers.CharField(max_length=64)
    nazwisko = serializers.CharField(max_length=128)
    plec = serializers.ChoiceField(choices=Gender.choices)
    stanowisko = serializers.PrimaryKeyRelatedField(queryset=Stanowisko.objects.all())
    data_dodania = serializers.DateField()


class StanowiskoSerializer(serializers.Serializer):
    nazwa = serializers.CharField(read_only=True)
    opis = serializers.CharField(read_only=True)


class GenderSerializer(serializers.Serializer):
    nazwa = serializers.CharField(read_only=True)
