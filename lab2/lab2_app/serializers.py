from lab2_app.models import Osoba, Stanowisko, Gender
from rest_framework import serializers
from django.utils import timezone


class OsobaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Osoba
        fields = [
            'imie',
            'nazwisko',
            'plec',
            'stanowisko',
            'data_dodania']
        read_only_fields = ['wlasciciel']

    def create(self, validated_data):
        osoba = Osoba(**validated_data)
        osoba.save()
        return osoba

    def validate_imie(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Nazwa musi składać się tylko z liter!")
        return value

    def validate_data_dodania(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Data dodania nie może być z przyszłości")
        return value


class StanowiskoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stanowisko
        fields = ['id', 'nazwa', 'opis']
        read_only_fields = ['id']

    def create(self, validated_data):
        stanowisko = Stanowisko(**validated_data)
        stanowisko.save()
        return stanowisko


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'nazwa']
