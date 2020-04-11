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

