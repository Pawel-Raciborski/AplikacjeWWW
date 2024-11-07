from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lab2_app.models import Osoba, Stanowisko
from lab2_app.serializers import OsobaSerializer, StanowiskoSerializer


# Create your views here.

@api_view(['POST'])
def create_osoba(request):
    if request.method == 'POST':
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Osoba utworzona prawidłowo'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def get_osoba(request, id):
    try:
        person = Osoba.objects.get(pk=id)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        person = Osoba.objects.get(pk=id)
        serializer = OsobaSerializer(person)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        person = Osoba.objects.get(pk=id)
        serializer = OsobaSerializer(person)
        person.delete()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_osoba(request):
    if request.method == 'GET':
        people = Osoba.objects.all()
        serializer = OsobaSerializer(people, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_osoba_with_name(request):
    if request.method == 'GET':
        people_witch_specified_name = Osoba.objects.filter(imie__contains=request.GET.get('imie'))
        serializer = OsobaSerializer(people_witch_specified_name, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_stanowisko(request):
    if request.method == 'POST':
        serializer = StanowiskoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Stanowisko utworzone'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def get_stanowisko(request, pk):
    if request.method == 'GET':
        stanowisko = Stanowisko.objects.get(pk=pk)
        serializer = StanowiskoSerializer(stanowisko)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        stanowisko = Stanowisko.objects.get(pk=pk)
        serializer = StanowiskoSerializer(stanowisko)
        stanowisko.delete()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_stanowisko(request):
    if request.method == 'GET':
        all_stanowisko = Stanowisko.objects.all()
        serializer = StanowiskoSerializer(all_stanowisko, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
