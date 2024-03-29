# Projekat
Projekat predstavlja simulaciju rada bolnice. Radio se preko Django framework-a. Način komunikacije je server-klijent.

# Pokretanje i razvoj

Django je divan! Stoga, korišćen je Django. Python verzija potrebna za pokretanje
i razvoj je 3.6. Poželjno je koristiti virtualno okruženje jer stvari inače lako
mogu krenuti po zlu (koristili smo Powershell sa administatorskim privilegijama za izvršavanje ovih komandi). To bismo ovako nekako uradili:
```sh
python -m venv venv
```
i zatim to virtualno okruženje aktivirali:
```powershell
venv\Scripts\activate.ps1
```
Ako vam ne daje da pokrenete script onda u powershell kao admin:
```powershell
set-executionpolicy remotesigned
```
Sa aktiviranim virtualnim okruženjem konačno možemo da instaliramo potrebne pakete
(ovde instaliramo Django!):
```powershell
pip install -r requirements.txt
```
Mora i:
```powershell
pip install six
```
```powershell
pip install django-extensions
```
Za bazu PostgresSQL mora:
```powershell
pip install psycopg2
```
Mora da se ako nemate, napraviti database tj. baza podataka gde će se čuvati informacije. Bazu podataka možete napraviti preko PostgesSQL programa (https://www.enterprisedb.com/downloads/postgres-postgresql-downloads).
Stavljeno je u programu da naziv baze, naziv korisnika kao i šifra sve bude "postgres", ako vam to ne odgovara možete jednostavno promeniti u settings.py koji se nalazi u eir/eir. Posle toga važno je da se ove komande izvrše:
```powershell
python manage.py makemigrations
```
pa:
```powershell
python manage.py migrate
```
Ako ima nekih problema kod migrate možete da ovo stavite:
```powershell
python manage.py showmigrations
```
Preko nje ćete videti koja je migracija prošla a koja nije.
Aplikacija se onda može pokrenuti jednim jednostavnim
```powershell
python manage.py runserver
```
Skripta se pokreće preko:
```powershell
python manage.py runscript ucitajSkriptu
```
Imate i superuser-a preko kojeg možete da vidite sve podatke:
```
python manage.py createsuperuser
```
Zatim da biste mu pristupili idete na:
*adresa servera/admin*

P.S. Ako lekar/admin zele da pogledaju svoj profil, treba da pritisnu na dugme sa svojim imenom i prezimenom u gornjem desnom uglu

# Autori
- Jovan Ćorilić (SW 48/2017) 
- Bogdan Čiplić (SW 79/2017)
- Mladen Samardžić (SW 37/2017) - Napustio
