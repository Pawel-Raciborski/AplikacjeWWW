from lab2_app.models import Osoba, Stanowisko, Gender
from rest_framework import serializers
from django.utils import timezone


class OsobaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    imie = serializers.CharField(max_length=64)
    nazwisko = serializers.CharField(max_length=128)
    plec = serializers.ChoiceField(choices=Gender.choices)
    stanowisko = serializers.PrimaryKeyRelatedField(queryset=Stanowisko.objects.all())
    data_dodania = serializers.DateField()

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


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'nazwa']
