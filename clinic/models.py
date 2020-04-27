from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


class Snippet(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def body_preview(self):
        return self.body[:50]


class Pacijent(models.Model):
    email_adresa = models.CharField(max_length=500, primary_key=True, default=None)
    lozinka = models.CharField(max_length=500, default=None)
    ime = models.CharField(max_length=500, default=None)
    prezime = models.CharField(max_length=500, default=None)
    adresa_prebivalista = models.CharField(max_length=500, default=None)
    grad = models.CharField(max_length=500, default=None)
    drzava = models.CharField(max_length=500, default=None)
    broja_telefona = models.CharField(max_length=500, default=None)
    jedinstveni_broj_osiguranika = models.CharField(max_length=500, default=None)
    sifra_bolesti = models.CharField(max_length=500, default=None)
    datum = models.CharField(max_length=500, default=None)
    diagnoza = models.CharField(max_length=500, default=None)
    lekovi = models.CharField(max_length=500, default=None)
    dioptrija = models.CharField(max_length=500, default=None)
    alergije_na_lek = models.CharField(max_length=500, default=None)
    visina = models.CharField(max_length=500, default=None)
    tezina = models.CharField(max_length=500, default=None)
    krvna_grupa = models.CharField(max_length=500, default=None)

    objects = UserManager()

    def __str__(self):
        return self.email_adresa


class Lekar(models.Model):
    email_adresa = models.TextField(max_length=500, default=None)
    lozinka = models.TextField(max_length=500, default=None)
    ime = models.TextField(max_length=500, default=None)
    prezime = models.TextField(max_length=500)
    broja_telefona = models.TextField(max_length=500, default=None)
    jedinstveni_broj_osiguranika = models.TextField(max_length=500, default=None)
    datum = models.DateTimeField(max_length=500, default=None)
    radno_mesto = models.TextField(max_length=500, default=None)
    pozicija = models.TextField(max_length=500, default=None)

    def __str__(self):
        return self.email_adresa

class Admin(models.Model):
    email_adresa = models.TextField(max_length=500, default=None)
    lozinka = models.TextField(max_length=500, default=None)
    ime = models.TextField(max_length=500, default=None)
    prezime = models.TextField(max_length=500, default=None)
    broja_telefona = models.TextField(max_length=500, default=None)
    jedinstveni_broj_osiguranika = models.TextField(max_length=500, default=None)
    datum = models.DateTimeField(max_length=500, default=None)
    naziv_klinike = models.TextField(max_length=500, default=None)

    objects = UserManager()

    def __str__(self):
        return self.email_adresa

class Sala(models.Model):
    broj = models.TextField(max_length=500, default=None)
    naziv = models.TextField(max_length=500, default=None)
    id_klinike_kojoj_pripada = models.TextField(max_length=500, default=None)
    opis = models.TextField(max_length=500, default=None)

    def __str__(self):
        return self.broj + "-" + self.id_klinike_kojoj_pripada


class Klinika(models.Model):
    naziv = models.TextField(max_length=500, default=None)
    adresa = models.TextField(max_length=500, default=None)
    opis = models.TextField(max_length=500, default=None)

    def __str__(self):
        return self.adresa
