from django.shortcuts import render


def index(req):
    return render(req, 'index.html')

def register_clinic_admin(req):
    return render(req, 'superadmin/register.html')