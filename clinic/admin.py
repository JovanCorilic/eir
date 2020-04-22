from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Snippet, Pacijent

admin.site.site_header = "Klinika"


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ('created',)
    change_list_template = 'admin/snippets/snippets_chnage_list.html'


class PacijentAdmin(admin.ModelAdmin):
    list_display = ("email_adresa","lozinka", "ime", "prezime", "adresa_prebivalista", "grad", "drzava", "broja_telefona", "jedinstveni_broj_osiguranika", "sifra_bolesti","datum","diagnoza","lekovi","dioptrija","alergije_na_lek","visina","tezina","krvna_grupa")
    list_filter = ("ime", "prezime")
    search_fields = ("ime", "prezime")


class LekarAdmin(admin.ModelAdmin):
    list_display = ("email_adresa","lozinka", "ime", "prezime", "broja_telefona", "jedinstveni_broj_osiguranika", "jedinstveni_broj_osiguranika", "radno_mesto", "pozicija")
    list_filter = ("ime", "prezime", "pozicija", "radno_mesto")
    search_fields = ("ime", "prezime", "pozicija", "radno_mesto")


class SalaAdmin(admin.ModelAdmin):
    list_display = ("broj", "naziv", "id_klinike_kojoj_pripada", "opis")
    list_filter = ("broj", "naziv", "id_klinike_kojoj_pripada")
    search_fields = ("broj", "naziv", "id_klinike_kojoj_pripada", "opis")


class KlinikaAdmin(admin.ModelAdmin):
    list_display = ("naziv", "adresa", "opis")
    list_filter = ("naziv")
    search_fields = ("ime", "adresa", "opis")


admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Pacijent, PacijentAdmin)
admin.site.unregister(Group)
