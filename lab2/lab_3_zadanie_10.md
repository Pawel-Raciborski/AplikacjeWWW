# Zapytania

### Wyświetl wszystkie obiekty modelu Osoba,

```python
from lab2_app.models import Osoba      
osoby = Osoba.objects.all()
print(osoby)
```

### Wyświetl obiekt modelu Osoba z id = 3,

```python
from lab2_app.models import Osoba      
osoba_id3=Osoba.objects.get(id=3)
print(osoba_id3)
```

### Wyświetl obiekty modelu Osoba, których nazwa rozpoczyna się na wybraną przez Ciebie literę alfabetu (tak, żeby był co najmniej jeden wynik)

```python
from lab2_app.models import Osoba
osoby = Osoba.objects.filter(imie__startswith='A')
print(osoby)
```

### Wyświetl unikalną listę stanowisk przypisanych dla modeli Osoba,

```python
from lab2_app.models import Stanowisko;
Stanowisko.objects.filter(osoba__isnull=False).distinct()
```

### Wyświetl nazwy stanowisk posortowane alfabetycznie malejąco

```python
from lab2_app.models import Stanowisko;
Stanowisko.objects.order_by('-nazwa')
```

### Dodaj nową instancję obiektu klasy Osoba i zapisz w bazie.

```python
from lab2_app.models import Osoba
nowa_osoba = Osoba.objects.create(imie="Paweł",nazwisko='Pawlak',stanowisko_id=2,plec=1)
nowa_osoba.save()
```