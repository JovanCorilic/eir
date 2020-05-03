from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('', views.index),
    path('superadmin/register', views.register_clinic_admin),
    path('login', views.login_pacijent),
    path('pacijent/registracijaPacijent', views.registracijaPacijent,  name='registracijaPacijent'),
    path('pacijent/loginPacijent', views.loginPacijent, name = 'loginPacijent'),
    path('pacijent/glavnaStranicaPacijent', views.glavnaStranicaPacijent, name = 'glavnaStranicaPacijent'),
    path('pacijent/licniPodaciPacijent', views.licniPodaciPacijent, name = 'licniPodaciPacijent'),
    path('pacijent/promenaLicniPodaciPacijent', views.promenaLicniPodaciPacijent, name = 'promenaLicniPodaciPacijent'),
    path('pacijent/zdravstveniKartonPacijent', views.zdravstveniKartonPacijent, name = 'zdravstveniKartonPacijent'),
    path('pacijent/prikazKlinikaPacijent', views.prikazKlinikaPacijent, name = 'prikazKlinikaPacijent'),
    path('pacijent/prikazLekaraKlinikePacijent', views.prikazLekaraKlinikePacijent, name = 'prikazLekaraKlinikePacijent'),
    path('lekar/izmeni', views.izmeni_lekara),
    path('sala/izmeni', views.izmeni_salu),
    path('klinika/izmeni', views.izmeni_kliniku),
    path('registerLekara', views.registerLekara, name='registerLekara'),
    path('registerLekar', views.registerLekara, name='registerLekar'),# vraca error ako obrisem
    path('registerAdmina', views.registerAdmina, name='registerAdmina'),
    path('promeniLozinku', views.promeniLozinku, name='promeniLozinku'),
    path('IzlogujSe', views.IzlogujSe, name='IzlogujSe'),
    path('Omeni', views.Omeni, name='Omeni'),
    path('IzmeniKorisnika', views.IzmeniKorisnika, name='IzmeniKorisnika'),
    path('pogledajPacijente', views.pogledajPacijente, name='pogledajPacijente'),
    path('PogledajPacijenta', views.PogledajPacijenta, name='PogledajPacijenta'),
    path('pogledajSale', views.pogledajSale, name='pogledajSale'),
    path('pogledajSalu', views.pogledajSalu, name='pogledajSalu'),
    path('IzmeniSalu', views.IzmeniSalu, name='IzmeniSalu'),
    path('ObrisiSalu', views.ObrisiSalu, name='ObrisiSalu'),
    path('DodajSalu', views.DodajSalu, name='DodajSalu'),
    path('pogledajKlinike', views.pogledajKlinike, name='pogledajKlinike'),
    path('pogledajKliniku', views.pogledajKliniku, name='pogledajKliniku'),
    path('IzmeniKliniku', views.IzmeniKliniku, name='IzmeniKliniku'),
    path('pogledajLekare', views.pogledajLekare, name='pogledajLekare'),
    path('PogledajLekara', views.PogledajLekara, name='PogledajLekara'),
    path('IzmeniLekara', views.IzmeniLekara, name='IzmeniLekara'),
    path('ObrisiLekara', views.ObrisiLekara, name='ObrisiLekara'),
]
