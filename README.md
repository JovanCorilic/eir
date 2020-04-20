# [Eir](https://en.wikipedia.org/wiki/Eir)

<em>
hiljadu osam <br>
brojim misli o tebi <br>
hiljadu devet
</em>

# Pokretanje i razvoj

Django je divan! Stoga, korišćen je Django. Python verzija potrebna za pokretanje
i razvoj je 3.6. Poželjno je koristiti virtualno okruženje jer stvari inače lako
mogu krenuti po zlu. To bismo ovako nekako uradili:
```sh
python -m venv venv
```
i zatim to virtualno okruženje aktivirali. Ako ste na Linuksu:
```sh
source venv/bin/activate
```
ili pak na svojoj Windows mašini:
```powershell
venv\Scripts\activate.ps1
```
Ako vam ne daje da pokrenete script onda u powershell kao admin:
```
set-executionpolicy remotesigned
```
Sa aktiviranim virtualnim okruženjem konačno možemo da instaliramo potrebne pakete
(ovde instaliramo Django!):
```sh
pip install -r requirements.txt
```
I za bazu PostgresSQL mora:
```
pip install psycopg2
```
Aplikacija se onda može pokrenuti jednim jednostavnim
```sh
python manage.py runserver
```

# Autori
- Bogdan Čiplić (SW 79/2017)
- Jovan Ćorilić (SW 48/2017)
- Mladen Samardžić (SW 37/2017) - Napustio
