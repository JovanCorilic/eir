from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from clinic.models import Pacijent
from django.contrib import messages
from datetime import date


# Create your views here.
def register(request):
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

        if Pacijent.objects.filter(email_adresa=email_adresa).exists():
            print("Email adresa je vec zauzeta")
            messages.info(request, "Email adresa je vec zauzeta")
            return redirect('register')

        pacijent = Pacijent.objects.create(email_adresa=email_adresa, lozinka=lozinka, ime=ime, prezime=prezime,
                                           adresa_prebivalista=adresa_prebivalista, grad=grad, drzava=drzava,
                                           broja_telefona=broja_telefona,
                                           jedinstveni_broj_osiguranika=jedinstveni_broj_osiguranika,
                                           alergije_na_lek="TBA", datum=date.today(), diagnoza="TBA", dioptrija="N/A",
                                           krvna_grupa="TBA", lekovi="N/A", sifra_bolesti="N/A", tezina=0, visina=0)
        pacijent.save()
        return redirect('login')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email_adresa = request.POST['email']
        lozinka = request.POST['password']
        # user = auth.authenticate(email_adresa=email_adresa, lozinka=lozinka)
        # if user is not None:
        #    auth.login(request, user)
        #    return redirect('/')

        print("Login email_adresa = " + email_adresa + ", i lozinka = " + lozinka + ",")
        print("Tacni username i password? -> " + str(Pacijent.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists()))
        if Pacijent.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists():
            print("Ulogovan kao " + Pacijent.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime)
            sadrzaj = {
                "ime": Pacijent.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime,#p,
                "email": email_adresa,
            }
            print(Pacijent.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime)
            return render(request, 'index.html', sadrzaj)
        else:
            messages.info(request, "Pogrešno korisničko ime ili lozinka")
            return redirect('login')
    else:
        return render(request, 'login.html')
