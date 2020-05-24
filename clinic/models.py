from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
import datetime

class Snippet(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def body_preview(self):
        return self.body[:50]





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
    ocena = models.FloatField(default=-1)

    objects = UserManager()

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

    objects = UserManager()

    def __str__(self):
        return self.broj + "-" + self.id_klinike_kojoj_pripada


class Klinika(models.Model):
    naziv = models.TextField(max_length=500, default=None)
    adresa = models.TextField(max_length=500, default=None)
    opis = models.TextField(max_length=500, default=None)
    ocena = models.FloatField(default=-1)

    objects = UserManager()

    def __str__(self):
        return self.adresa








class Odmor(models.Model):
    id = models.CharField(max_length=500, primary_key=True,  default=None)
    klinika = models.CharField(max_length=500, default=None)
    lekar = models.CharField(max_length=500, default=None)
    vreme = models.DateTimeField(max_length=500, default=None)
    duzina = models.IntegerField(default=10)
    aktiviran = models.IntegerField(default=0)

    objects = UserManager()

    def __str__(self):
        return self.lekar.__str__() + " ima odmor " + self.vreme.__str__() + " od " + self.duzina.__str__() + " dana"

