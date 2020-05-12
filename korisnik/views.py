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
            request.session['email'] = email_adresa
            temp = list(Pacijent.objects.filter(email_adresa=email_adresa).values())
            recnik = temp[0]
            request.session['lozinka'] = lozinka
            # ime = recnik.get('ime')

            print(recnik.get('aktiviran'))
            if not recnik.get('aktiviran') == 1:
                messages.info(request, "Email koji ste uneli nije još verifikovan!")
                return redirect('loginKorisnik')

            request.session['ime'] = recnik.get('ime')
            request.session['prezime'] = recnik.get('prezime')
            request.session['adresa_prebivalista'] = recnik.get('adresa_prebivalista')
            request.session['grad'] = recnik.get('grad')
            request.session['drzava'] = recnik.get('drzava')
            request.session['broja_telefona'] = recnik.get('broja_telefona')
            request.session['jedinstveni_broj_osiguranika'] = recnik.get('jedinstveni_broj_osiguranika')
            request.session['sifra_bolesti'] = recnik.get('sifra_bolesti')
            request.session['datum'] = recnik.get('datum')
            request.session['diagnoza'] = recnik.get('diagnoza')
            request.session['lekovi'] = recnik.get('lekovi')
            request.session['dioptrija'] = recnik.get('dioptrija')
            request.session['alergije_na_lek'] = recnik.get('alergije_na_lek')
            request.session['visina'] = recnik.get('visina')
            request.session['tezina'] = recnik.get('tezina')
            request.session['krvna_grupa'] = recnik.get('krvna_grupa')
            request.session['ulogovan'] = 'true'
            request.session['lokacija'] = 0
            return render(request, 'glavnaStranicaPacijent.html',
                          {'email': request.session['email'], 'ime': request.session['ime'],
                           'prezime': request.session['prezime'],
                           'lokacija': request.session['lokacija']})
        elif Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists():
            print("Ulogovan kao " + Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime)
            #sadrzaj = {
            #    "ime": Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime,
            #    "email": email_adresa,
            #    "uloga": "LEKAR"
            #}
            #response = redirect('/')
            #request.session['email'] = email_adresa
            #return render(request, 'index.html', sadrzaj)
            request.session['ime'] = Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime
            request.session['email'] = email_adresa
            request.session['uloga'] = "LEKAR"
            request.session['prezime'] = Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].prezime
            request.session['ulogovan'] = 'true'
            return redirect('index')
        elif Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka).exists():
            print("Ulogovan kao " + Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime)
            #sadrzaj = {
            #    "ime": Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime,
            #    "email": email_adresa,
            #    "uloga": "ADMIN"
            #}
            #response = redirect('/')
            #request.session['email'] = email_adresa
            #return render(request, 'index.html', sadrzaj)
            request.session['ime'] = Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime
            request.session['email'] = email_adresa
            request.session['uloga'] = "ADMIN"
            request.session['prezime'] = Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].prezime
            request.session['ulogovan'] = 'true'
            return redirect('index')
        else:
            messages.info(request, "Pogrešno korisničko ime ili lozinka")
            return redirect('loginKorisnik')
    else:
        uloga = ""
        if 'uloga' in request.session:
            uloga = request.session['uloga']
        return render(request, 'login.html', {'uloga': uloga,})
