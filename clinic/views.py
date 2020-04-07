from django.shortcuts import render


def index(req):
    return render(req, 'index.html')

def register_clinic_admin(req):
    return render(req, 'superadmin/register.html')

def login_pacijent(req):
    return render(req, 'login.html')

def glavna_stranica_pacijent(req):
    return render(req, 'pacijent/glavnaStranica.html')