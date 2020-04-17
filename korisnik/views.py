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
            messages.info(request, "Email adresa je vec zauzeta")
            return redirect('register')

        pacijent = Pacijent.objects.create(email_adresa=email_adresa, lozinka=lozinka, ime=ime, prezime=prezime, adresa_prebivalista=adresa_prebivalista, grad=grad, drzava=drzava, broja_telefona=broja_telefona,jedinstveni_broj_osiguranika=jedinstveni_broj_osiguranika, alergije_na_lek="TBA", datum=date.today(), diagnoza="TBA", dioptrija="N/A", krvna_grupa="TBA", lekovi="N/A", sifra_bolesti="N/A", tezina=0, visina=0 )
        pacijent.save()
        return redirect('/')
    else:
        return render(request, 'register.html')
