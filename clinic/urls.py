from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('superadmin/register', views.register_clinic_admin),
    path('login', views.login_pacijent),
    path('pacijent/registracija', views.registracija_pacijent),
    path('pacijent/glavnaStranica', views.glavna_stranica_pacijent),
    path('lekar/izmeni', views.izmeni_lekara),
    path('sala/izmeni', views.izmeni_salu),
    path('klinika/izmeni', views.izmeni_kliniku),
]
