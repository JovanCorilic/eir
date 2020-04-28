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
    path('lekar/izmeni', views.izmeni_lekara),
    path('sala/izmeni', views.izmeni_salu),
    path('klinika/izmeni', views.izmeni_kliniku),
    path('registerLekara', views.registerLekara, name='registerLekara'),
    path('registerLekar', views.registerLekara, name='registerLekar'),# vraca error ako obrisem
    path('registerAdmina', views.registerAdmina, name='registerAdmina'),
    path('promeniLozinku', views.promeniLozinku, name='promeniLozinku'),
    path('IzlogujSe', views.IzlogujSe, name='IzlogujSe'),
]
