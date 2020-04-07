from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('superadmin/register', views.register_clinic_admin),
    path('login', views.login_pacijent),
    path('pacijent/glavnaStranica', views.glavna_stranica_pacijent)
]