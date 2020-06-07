from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
import datetime


# Create your models here.

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
    aktiviran = models.IntegerField(default=1)

    objects = UserManager()

    def __str__(self):
        return self.email_adresa


class Pregled(models.Model):
    id = models.CharField(max_length=500, primary_key=True, default=None)
    klinika = models.CharField(max_length=500, default=None)
    zakazan = models.CharField(max_length=500, default=None)
    lekar = models.CharField(max_length=500, default=None)
    sala = models.CharField(max_length=500, default=None)
    tip_pregleda = models.CharField(max_length=500, default=None)
    vreme = models.DateTimeField(max_length=500, default=None)
    sifra_bolesti = models.CharField(max_length=500, default=None)
    diagnoza = models.CharField(max_length=500, default=None)
    lekovi = models.CharField(max_length=500, default=None)
    temp = "da"
    prihvacen = models.CharField(max_length=500, default="da")
    ocenaLekara = models.FloatField(default=-1)
    ocenaKlinike = models.FloatField(default=-1)

    objects = UserManager()


class Operacije(models.Model):
    id = models.CharField(max_length=500, primary_key=True, default=None)
    klinika = models.CharField(max_length=500, default=None)
    pacijent = models.CharField(max_length=500, default=None)
    lekari = models.CharField(max_length=500, default=None)
    sala = models.CharField(max_length=500, default=None)
    tip_operacije = models.CharField(max_length=500, default=None)
    vreme = models.DateTimeField(max_length=500, default=None)
    ocenaLekara = models.CharField(max_length=500, default="-1")
    ocenaKlinike = models.FloatField(default=-1)

    objects = UserManager()
