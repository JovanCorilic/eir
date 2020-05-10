from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Snippet, Pacijent,Lekar,Sala,Klinika,Admin,Pregled

admin.site.site_header = "Klinika"


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ('created',)
    change_list_template = 'admin/snippets/snippets_chnage_list.html'


class PacijentAdmin(admin.ModelAdmin):
    list_display = ("email_adresa","lozinka", "ime", "prezime", "adresa_prebivalista", "grad", "drzava", "broja_telefona", "jedinstveni_broj_osiguranika", "sifra_bolesti","datum","diagnoza","lekovi","dioptrija","alergije_na_lek","visina","tezina","krvna_grupa")
    list_filter = ("ime", "prezime","email_adresa","lozinka")
    search_fields = ("ime", "prezime")


class LekarAdmin(admin.ModelAdmin):
    list_display = ("email_adresa","lozinka", "ime", "prezime", "broja_telefona", "jedinstveni_broj_osiguranika", "radno_mesto", "pozicija")
    list_filter = ("ime", "prezime", "pozicija", "radno_mesto","email_adresa","lozinka")
    search_fields = ("ime", "prezime", "pozicija", "radno_mesto")


class SalaAdmin(admin.ModelAdmin):
    list_display = ("broj", "naziv", "id_klinike_kojoj_pripada", "opis")
    list_filter = ("broj", "naziv", "id_klinike_kojoj_pripada")
    search_fields = ("broj", "naziv", "id_klinike_kojoj_pripada", "opis")


class KlinikaAdmin(admin.ModelAdmin):
    list_display = ("naziv", "adresa", "opis")
    list_filter = ("naziv", "opis")
    search_fields = ("ime", "adresa", "opis")

class AdminAdmin(admin.ModelAdmin):
    list_display = ("email_adresa","lozinka", "ime", "prezime", "broja_telefona", "jedinstveni_broj_osiguranika", "datum", "naziv_klinike")
    list_filter = ("ime", "prezime","email_adresa","lozinka")
    search_fields = ("ime", "prezime")

class PregledAdmin(admin.ModelAdmin):
    list_display = ("id", "klinika", "zakazan", "lekar", "sala", "tip_pregleda", "vreme", "sifra_bolesti", "lekovi", "diagnoza", "temp")
    list_filter = ("id", "klinika", "lekar", "tip_pregleda", "sala")
    search_fields = ("id", "klinika", "lekar", "tip_pregleda", "sala")

admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Pacijent, PacijentAdmin)
admin.site.register(Lekar,LekarAdmin)
admin.site.register(Sala,SalaAdmin)
admin.site.register(Klinika,KlinikaAdmin)
admin.site.register(Admin,AdminAdmin)
admin.site.register(Pregled, PregledAdmin)
admin.site.unregister(Group)
