import csv

from clinic.models import Lekar, Klinika, Sala, Admin, Odmor
from pacijent.models import Pregled, Pacijent, TipPregleda
from datetime import datetime

def run():
    kratko = open('skripta.csv', encoding='unicode_escape')
    reader = csv.reader(kratko)

    Pacijent.objects.all().delete()
    Klinika.objects.all().delete()
    Sala.objects.all().delete()
    Admin.objects.all().delete()
    Lekar.objects.all().delete()
    TipPregleda.objects.all().delete()
    Pregled.objects.all().delete()

    for row in reader:
        print(row)
        print("\n")
        print(row[0],row[1],row[2])
        if("Pacijent" in row[0]):
            pacijent = Pacijent.objects.create(email_adresa=row[1], lozinka=row[2], ime=row[3], prezime=row[4],
                                               broja_telefona=row[5],
                                               jedinstveni_broj_osiguranika=row[6],
                                               adresa_prebivalista=row[7], grad=row[8], drzava=row[9],
                                               sifra_bolesti=row[10], datum=row[11],
                                               diagnoza=row[12], lekovi=row[13],
                                               dioptrija=row[14], alergije_na_lek=row[15],
                                               visina=row[16], tezina=row[17], krvna_grupa=row[18], aktiviran=row[19])

            pacijent.save()
        elif ("TipPregleda" in row[0]):
            tipPregleda = TipPregleda.objects.create(id=row[1], ime=row[2], cena=row[3], trajanje=row[4])
            tipPregleda.save()
        elif("Klinika" in row[0]):
            klinika = Klinika.objects.create(naziv=row[1], adresa=row[2], opis=row[3], ocena=float(row[4]))
            klinika.save()
        elif("Sala"in row[0]):
            sala = Sala.objects.create(broj=row[1], naziv=row[2], id_klinike_kojoj_pripada=row[3], opis=row[4])
            sala.save()
        elif("Lekar"in row[0]):
            lekar = Lekar.objects.create(email_adresa=row[1], lozinka=row[2], ime=row[3], prezime=row[4], broja_telefona=row[5], jedinstveni_broj_osiguranika=row[6],
                                         datum=datetime.strptime(row[7], "%d/%m/%Y %I:%M%p"), radno_mesto=row[8], pozicija=row[9], ocena=float(row[10]))
            lekar.save()
        elif("Admin"in row[0]):
            admin = Admin.objects.create(email_adresa=row[1], lozinka=row[2], ime=row[3], prezime=row[4], broja_telefona=row[5], jedinstveni_broj_osiguranika=row[6],
                                         datum=datetime.strptime(row[7], "%d/%m/%Y %I:%M%p"), naziv_klinike = row[8])
            admin.save()
        elif("Pregled"in row[0]):
            pregled = Pregled.objects.create(id=row[1], klinika=row[2], zakazan=row[3], lekar=row[4], sala=row[5],
                                             tip_pregleda = row[6], vreme= datetime.strptime(row[7], "%d/%m/%Y %I:%M%p"), sifra_bolesti= row[8], diagnoza = row[9],
                                             lekovi=row[10])
            pregled.save()
