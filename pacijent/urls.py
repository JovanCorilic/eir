
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [

    path('pacijent/registracijaPacijent', views.registracijaPacijent, name='registracijaPacijent'),
    path('pacijent/glavnaStranicaPacijent', views.glavnaStranicaPacijent, name='glavnaStranicaPacijent'),
    path('pacijent/licniPodaciPacijent', views.licniPodaciPacijent, name='licniPodaciPacijent'),
    path('pacijent/promenaLicniPodaciPacijent', views.promenaLicniPodaciPacijent, name='promenaLicniPodaciPacijent'),
    path('pacijent/zdravstveniKartonPacijent', views.zdravstveniKartonPacijent, name='zdravstveniKartonPacijent'),
    path('pacijent/prikazKlinikaPacijent', views.prikazKlinikaPacijent, name='prikazKlinikaPacijent'),
    path('pacijent/prikazLekaraKlinikePacijent', views.prikazLekaraKlinikePacijent, name='prikazLekaraKlinikePacijent'),
    path('pacijent/prikazKlinikaPacijentSortirano', views.prikazKlinikaPacijentSortirano,
         name='prikazKlinikaPacijentSortirano'),
    path('pacijent/pretragaKlinikaPacijent', views.pretragaKlinikaPacijent, name='pretragaKlinikaPacijent'),
    path('pacijent/sortiranjeLekaraPacijent', views.sortiranjeLekaraPacijent, name='sortiranjeLekaraPacijent'),
    path('pacijent/pretragaLekaraPacijent', views.pretragaLekaraPacijent, name='pretragaLekaraPacijent'),
    path('pacijent/prikaziBrzePreglede', views.prikaziBrzePreglede, name='prikaziBrzePreglede'),
    path('pacijent/zakaziBrzPregled', views.zakaziBrzPregled, name='zakaziBrzPregled'),
    path('pacijent/sviPreglediPacijent', views.sviPreglediPacijent, name='sviPreglediPacijent'),
    path('pacijent/otkaziPregledPacijent', views.otkaziPregledPacijent, name='otkaziPregledPacijent'),
    path('pacijent/sveOperacijePacijent', views.sveOperacijePacijent, name='sveOperacijePacijent'),
    path('pacijent/sortiranjeSveOperacijePacijent', views.sortiranjeSveOperacijePacijent,
         name='sortiranjeSveOperacijePacijent'),
    path('pacijent/zakazivanjePregledaPacijent', views.zakazivanjePregledaPacijent, name='zakazivanjePregledaPacijent'),
    path('pacijent/posaljiPregledPacijent', views.posaljiPregledPacijent, name='posaljiPregledPacijent'),
    path('pacijent/prosliPreglediPacijent', views.prosliPreglediPacijent, name='prosliPreglediPacijent'),
    path('pacijent/oceniPregledPacijent', views.oceniPregledPacijent, name='oceniPregledPacijent'),
    path('pacijent/posaljiOcenuPacijent', views.posaljiOcenuPacijent, name='posaljiOcenuPacijent'),
    path('pacijent/oceniOperacijuPAcijent', views.oceniOperacijuPAcijent, name='oceniOperacijuPAcijent'),
    path('pacijent/posaljiOcenuOperacijaPacijent', views.posaljiOcenuOperacijaPacijent, name='posaljiOcenuOperacijaPacijent'),
    path('pacijent/vecZakazaniLekarPacijent', views.vecZakazaniLekarPacijent, name='vecZakazaniLekarPacijent'),


]
