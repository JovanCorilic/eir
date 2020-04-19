from django.shortcuts import render


def index(req):
    return render(req, 'index.html')


def register_clinic_admin(req):
    return render(req, 'superadmin/register.html')


def registracija_pacijent(req):
    return render(req, 'pacijent/registracija.html')


def login_pacijent(req):
    return render(req, 'login.html')


def glavna_stranica_pacijent(req):
    return render(req, 'pacijent/glavnaStranica.html')


def izmeni_lekara(req):
    return render(req, 'lekar/izmeniInformacijeLekara.html')


def izmeni_kliniku(req):
    return render(req, 'klinika/izmeniInformacijeKlinike.html')


def izmeni_salu(req):
    return render(req, 'sala/izmeniInformacijeSale.html')
