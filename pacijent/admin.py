from django.contrib import admin
from .models import Pacijent, Pregled, Operacije
# Register your models here.
class PacijentAdmin(admin.ModelAdmin):
    list_display = ("aktiviran", "email_adresa","lozinka", "ime", "prezime", "adresa_prebivalista", "grad", "drzava", "broja_telefona", "jedinstveni_broj_osiguranika", "sifra_bolesti","datum","diagnoza","lekovi","dioptrija","alergije_na_lek","visina","tezina","krvna_grupa")
    list_filter = ("ime", "prezime","email_adresa","lozinka")
    search_fields = ("ime", "prezime")

class PregledAdmin(admin.ModelAdmin):
    list_display = ("id", "klinika", "zakazan", "lekar", "sala", "tip_pregleda", "vreme", "sifra_bolesti", "lekovi", "diagnoza", "temp", "prihvacen")
    list_filter = ("id", "klinika", "lekar", "tip_pregleda", "sala")
    search_fields = ("id", "klinika", "lekar", "tip_pregleda", "sala")


class OperacijeAdmin(admin.ModelAdmin):
    list_display = ("id", "klinika", "pacijent", "lekari", "sala", "tip_operacije", "vreme")
    list_filter = ("id", "klinika", "tip_operacije", "sala")
    search_fields = ("id", "klinika", "tip_operacije", "sala")

admin.site.register(Pregled, PregledAdmin)
admin.site.register(Pacijent, PacijentAdmin)
admin.site.register(Operacije, OperacijeAdmin)