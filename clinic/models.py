from __future__ import unicode_literals
from django.db import models


class Snippet(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def body_preview(self):
        return self.body[:50]


class Pacijent(models.Model):
    email_adresa= models.CharField(max_length=500)
    lozinka= models.CharField(max_length=500)
    ime= models.CharField(max_length=500)
    prezime= models.CharField(max_length=500)
    adresa_prebivalista= models.CharField(max_length=500)
    grad= models.CharField(max_length=500)
    drzava= models.CharField(max_length=500)
    broja_telefona= models.CharField(max_length=500)
    jedinstveni_broj_osiguranika= models.CharField(max_length=500)
    sifra_bolesti= models.CharField(max_length=500)
    datum= models.DateTimeField(auto_now_add=True)
    diagnoza= models.CharField(max_length=500)
    lekovi= models.CharField(max_length=500)
    dioptrija= models.CharField(max_length=500)
    alergije_na_lek= models.CharField(max_length=500)
    visina= models.CharField(max_length=500)
    tezina= models.CharField(max_length=500)
    krvna_grupa= models.CharField(max_length=500)

    def __str__(self):
        return self.email_adresa


class Lekar(models.Model):
    email_adresa = models.TextField(max_length=500)
    lozinka = models.TextField(max_length=500)
    ime = models.TextField(max_length=500)
    prezime = models.TextField(max_length=500)
    broja_telefona = models.TextField(max_length=500)
    jedinstveni_broj_osiguranika = models.TextField(max_length=500)
    datum = models.DateTimeField(auto_now_add=True)
    radno_mesto = models.TextField(max_length=500)
    pozicija = models.TextField(max_length=500)

    def __str__(self):
        return self.email_adresa


class Sala(models.Model):
    broj = models.TextField(max_length=500)
    naziv = models.TextField(max_length=500)
    id_klinike_kojoj_pripada = models.TextField(max_length=500)
    opis = models.TextField(max_length=500)

    def __str__(self):
        return self.broj + "-" + self.id_klinike_kojoj_pripada


class Klinika(models.Model):
    naziv = models.TextField(max_length=500)
    adresa = models.TextField(max_length=500)
    opis = models.TextField(max_length=500)

    def __str__(self):
        return self.adresa
