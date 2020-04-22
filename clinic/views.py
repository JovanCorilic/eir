from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from clinic.models import Pacijent, Admin
from django.contrib import messages
from datetime import date
from clinic.models import Lekar


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

######################################################################################


def registerLekara(request):
    if request.method == 'POST':
        email_adresa = request.POST['email']
        lozinka = 'password'
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        broja_telefona = request.POST['btelefona']
        jedinstveni_broj_osiguranika = request.POST['jmbgnt']
        radno_mesto = "Nije implementirano"
        pozicija = request.POST['pozicija']

        if Admin.objects.filter(email_adresa=email_adresa).exists() or Pacijent.objects.filter(email_adresa=email_adresa).exists() or Lekar.objects.filter(email_adresa=email_adresa).exists():
            print("Email adresa je vec zauzeta")
            messages.info(request, "Email adresa je vec zauzeta")
            return redirect('registerLekara')

        elif "[" in ime or "]" in ime or "[NPL]" in ime:
            print("ime ne sme da sadrzi [NPL]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            return redirect('registerLekara')

        ime = "[NPL]" + ime

        lekar = Lekar.objects.create(email_adresa=email_adresa, lozinka=lozinka, ime=ime, prezime=prezime, broja_telefona=broja_telefona, jedinstveni_broj_osiguranika=jedinstveni_broj_osiguranika, datum=date.today(), radno_mesto=radno_mesto, pozicija=pozicija)
        lekar.save()
        print("napravljen lekar " + ime)
        return redirect('loginKorisnik')
    else:
        return render(request, 'registerLekara.html')


def registerAdmina(request):
    if request.method == 'POST':
        email_adresa = request.POST['email']
        lozinka = 'password'
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        broja_telefona = request.POST['btelefona']
        jedinstveni_broj_osiguranika = request.POST['jmbgnt']
        naziv_klinike = "Nije implementirano"

        if Admin.objects.filter(email_adresa=email_adresa).exists() or Pacijent.objects.filter(email_adresa=email_adresa).exists() or Lekar.objects.filter(email_adresa=email_adresa).exists():
            print("Email adresa je vec zauzeta")
            messages.info(request, "Email adresa je vec zauzeta")
            return redirect('registerLekara')

        elif "[" in ime or "]" in ime or "[NPL]" in ime:
            print("ime ne sme da sadrzi [NPL]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            return redirect('registerLekara')

        ime = "[NPL]" + ime

        admin = Admin.objects.create(email_adresa=email_adresa, lozinka=lozinka, ime=ime, prezime=prezime, broja_telefona=broja_telefona, jedinstveni_broj_osiguranika=jedinstveni_broj_osiguranika, datum=date.today(), naziv_klinike=naziv_klinike)
        admin.save()
        print("napravljen lekar " + ime)
        return redirect('loginKorisnik')
    else:
        return render(request, 'registerAdmina.html')


def promeniLozinku(request):
    if request.method == 'POST':
        lozinka = request.POST['password']
        email_adresa = request.POST['email']
        if Lekar.objects.filter(email_adresa=email_adresa).exists():
            lekar = Lekar.objects.filter(email_adresa=email_adresa)[0]
            lekar.ime = lekar.ime.replace("[NPL]", "")
            lekar.lozinka = lozinka

            lekar.save()

            sadrzaj = {
                "ime": Lekar.objects.filter(email_adresa=email_adresa)[0].ime,
                "email": Lekar.objects.filter(email_adresa=email_adresa)[0].email_adresa,
                "uloga": "LEKAR"
            }
            response = redirect('/')
            return render(request, 'index.html', sadrzaj)

        elif Admin.objects.filter(email_adresa=email_adresa).exists():
            admin = Admin.objects.filter(email_adresa=email_adresa)[0]
            admin.ime = admin.ime.replace("[NPL]", "")
            admin.lozinka = lozinka

            admin.save()

            sadrzaj = {
                "ime": Admin.objects.filter(email_adresa=email_adresa)[0].ime,
                "email": Admin.objects.filter(email_adresa=email_adresa)[0].email_adresa,
                "uloga": "LEKAR"
            }
            response = redirect('/')
            return render(request, 'index.html', sadrzaj)
        sadrzaj = {
            "ime": Lekar.objects.filter(email_adresa=request.POST['email'])[0].ime,
            "email": Lekar.objects.filter(email_adresa=request.POST['email'])[0].email_adresa,
            "uloga": "LEKAR"
        }
        response = redirect('/')
        return render(request, 'index.html', sadrzaj)
    else:
        sadrzaj = {
            "ime": Lekar.objects.filter(email_adresa=request.POST['email'])[0].ime,
            "email": Lekar.objects.filter(email_adresa=request.POST['email'])[0].email_adresa,
            "uloga": "LEKAR"
        }
        response = redirect('/')
        return render(request, 'index.html', sadrzaj)
