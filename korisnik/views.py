from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from clinic.models import Pacijent, Lekar, Admin
from django.contrib import messages
from datetime import date


# Create your views here.
def registerKorisnik(request):
    if request.method == 'POST':
        email_adresa = request.POST['email']
        lozinka = request.POST['password']
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        adresa_prebivalista = request.POST['adresa']
        grad = request.POST['grad']
        drzava = request.POST['drzava']
        broja_telefona = request.POST['btelefona']
        jedinstveni_broj_osiguranika = request.POST['jmbgnt']

        if Admin.objects.filter(email_adresa=email_adresa).exists() or Pacijent.objects.filter(email_adresa=email_adresa).exists() or Lekar.objects.filter(email_adresa=email_adresa).exists():
            print("Email adresa je vec zauzeta")
            messages.info(request, "Email adresa je vec zauzeta")
            return redirect('registerKorisnik')

        elif "[" in ime or "]" in ime or "[NPL]" in ime:
            print("ime ne sme da sadrzi [NPL]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            return redirect('registerLekara')

        pacijent = Pacijent.objects.create(email_adresa=email_adresa, lozinka=lozinka, ime=ime, prezime=prezime,
                                           adresa_prebivalista=adresa_prebivalista, grad=grad, drzava=drzava,
                                           broja_telefona=broja_telefona,
                                           jedinstveni_broj_osiguranika=jedinstveni_broj_osiguranika,
                                           alergije_na_lek="TBA", datum=date.today(), diagnoza="TBA", dioptrija="N/A",
                                           krvna_grupa="TBA", lekovi="N/A", sifra_bolesti="N/A", tezina=0, visina=0)
        pacijent.save()
        storage = messages.get_messages(request)
        storage.used = True
        return redirect('loginKorisnik')
    else:
        return render(request, 'register.html')


def loginKorisnik(request):
    if request.method == 'POST':
        email_adresa = request.POST['email']
        lozinka = request.POST['password']
        # user = auth.authenticate(email_adresa=email_adresa, lozinka=lozinka)
        # if user is not None:
        #    auth.login(request, user)
        #    return redirect('/')

        print("Login email_adresa = " + email_adresa + ", i lozinka = " + lozinka + ",")
        print("Tacni username i password za PACIJENT? -> " + str(Pacijent.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists()))
        print("Tacni username i password za LEKAR? -> " + str(Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists()))
        print("Tacni username i password za ADMIN? -> " + str(Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists()))
        if Pacijent.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists():
            print("Ulogovan kao " + Pacijent.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime)
            sadrzaj = {
                "ime": Pacijent.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime,
                "email": email_adresa,
                "uloga": "PACIJENT"
            }
            response = redirect('/')
            return render(request, 'index.html', sadrzaj)
        elif Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists():
            print("Ulogovan kao " + Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime)
            sadrzaj = {
                "ime": Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime,
                "email": email_adresa,
                "uloga": "LEKAR"
            }
            response = redirect('/')
            request.session['email'] = email_adresa
            return render(request, 'index.html', sadrzaj)
        elif Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists():
            print("Ulogovan kao " + Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime)
            sadrzaj = {
                "ime": Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime,
                "email": email_adresa,
                "uloga": "ADMIN"
            }
            response = redirect('/')
            request.session['email'] = email_adresa
            return render(request, 'index.html', sadrzaj)
        else:
            messages.info(request, "Pogrešno korisničko ime ili lozinka")
            return redirect('loginKorisnik')
    else:
        return render(request, 'login.html')
