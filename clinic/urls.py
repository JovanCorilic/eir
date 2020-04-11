from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('superadmin/register', views.register_clinic_admin),
    path('login', views.login_pacijent),
    path('pacijent/glavnaStranica', views.glavna_stranica_pacijent)
]