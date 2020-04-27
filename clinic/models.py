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
    email_adresa = models.CharField(max_length=500, primary_key=True)
    lozinka = models.CharField(max_length=500)
    ime = models.CharField(max_length=500)
    prezime = models.CharField(max_length=500)
    adresa_prebivalista = models.CharField(max_length=500)
    grad = models.CharField(max_length=500)
    drzava = models.CharField(max_length=500)
    broja_telefona = models.CharField(max_length=500)
    jedinstveni_broj_osiguranika = models.CharField(max_length=500)
    sifra_bolesti = models.CharField(max_length=500, default=None)
    datum = models.DateTimeField(max_length=500, default=None)
    diagnoza = models.CharField(max_length=500, default=None)
    lekovi = models.CharField(max_length=500, default=None)
    dioptrija = models.CharField(max_length=500, default=None)
    alergije_na_lek = models.CharField(max_length=500, default=None)
    visina = models.FloatField(max_length=500, default=None)
    tezina = models.FloatField(max_length=500, default=None)
    krvna_grupa = models.CharField(max_length=3, default=None)

    objects = UserManager()

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

    objects = UserManager()

    def __str__(self):
        return self.email_adresa


class Admin(models.Model):
    email_adresa = models.TextField(max_length=500)
    lozinka = models.TextField(max_length=500)
    ime = models.TextField(max_length=500)
    prezime = models.TextField(max_length=500)
    broja_telefona = models.TextField(max_length=500)
    jedinstveni_broj_osiguranika = models.TextField(max_length=500)
    datum = models.DateTimeField(auto_now_add=True)
    naziv_klinike = models.TextField(max_length=500)

    objects = UserManager()

    def __str__(self):
        return self.email_adresa


class Sala(models.Model):
    broj = models.TextField(max_length=500)
    naziv = models.TextField(max_length=500)
    id_klinike_kojoj_pripada = models.TextField(max_length=500)
    opis = models.TextField(max_length=500)

    objects = UserManager()

    def __str__(self):
        return self.broj + "-" + self.id_klinike_kojoj_pripada


class Klinika(models.Model):
    naziv = models.TextField(max_length=500)
    adresa = models.TextField(max_length=500)
    opis = models.TextField(max_length=500)

    objects = UserManager()

    def __str__(self):
        return self.adresa
