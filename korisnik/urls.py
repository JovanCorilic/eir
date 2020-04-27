from django.urls import path
from . import views

urlpatterns = [
    path("registerKorisnik", views.registerKorisnik, name="registerKorisnik"),
    path("loginKorisnik", views.loginKorisnik, name="loginKorisnik"),
]
