import graphene
from graphene_django import DjangoObjectType

from lab2_app.models import Osoba, Stanowisko


class OsobaType(DjangoObjectType):
    class Meta:
        model = Osoba
        fields = '__all__'


class Query(graphene.ObjectType):
    people = graphene.List(OsobaType)

    osoby_with_stanowisko = graphene.List(OsobaType, stanowisko_name=graphene.String(required=True))
    count_osoby = graphene.Int()

    def resolve_people(root, info):
        return Osoba.objects.all()

    def resolve_osoby_with_stanowisko(root, info, stanowisko_name):
        return Osoba.objects.filter(stanowisko__nazwa=stanowisko_name)

    def resolve_count_osoby(root, info):
        return Osoba.objects.count()

schema = graphene.Schema(query=Query)
