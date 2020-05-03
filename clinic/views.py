
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from clinic.models import Pacijent, Admin, Klinika
from django.contrib import messages
from datetime import date
from clinic.models import Lekar
from clinic.models import Sala


def index(req):
    ime = ""  # ako ne postoji
    email = ""
    uloga = ""
    prezime = ""
    if 'ime' in req.session:
        ime = req.session['ime']
    if 'email' in req.session:
        email = req.session['email']
    if 'uloga' in req.session:
        uloga = req.session['uloga']
    if 'prezime' in req.session:
        prezime = req.session['prezime']

    return render(req, 'index.html', {'ime': ime, 'email': email, 'uloga': uloga, 'prezime': prezime})


def IzlogujSe(request):
    ime = ""  # ako ne postoji
    email = ""
    uloga = ""
    request.session['ime'] = ''
    request.session['email'] = ''
    request.session['uloga'] = 'NEULOGOVAN'
    del request.session['ulogovan']
    return render(request, 'index.html', {'ime': ime, 'email': email, 'uloga': uloga})


def register_clinic_admin(req):
    return render(req, 'superadmin/register.html')


# def registracija_pacijent(req):
#   return render(req, 'pacijent/registracija.html')

# def login_pacijent2(req):
#   return  render(req, 'pacijent/login.html')


def login_pacijent(req):
    return render(req, 'login.html')


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
        radno_mesto = request.POST['radnomesto']
        pozicija = request.POST['pozicija']

        if Admin.objects.filter(email_adresa=email_adresa).exists() or Pacijent.objects.filter(
                email_adresa=email_adresa).exists() or Lekar.objects.filter(email_adresa=email_adresa).exists():
            print("Email adresa je vec zauzeta")
            messages.info(request, "Email adresa je vec zauzeta")
            return redirect('registerLekara')

        elif "[" in ime or "]" in ime or "[NPL]" in ime:
            print("ime ne sme da sadrzi [NPL]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            return redirect('registerLekara')

        ime = "[NPL]" + ime

        lekar = Lekar.objects.create(email_adresa=email_adresa, lozinka=lozinka, ime=ime, prezime=prezime,
                                     broja_telefona=broja_telefona,
                                     jedinstveni_broj_osiguranika=jedinstveni_broj_osiguranika, datum=date.today(),
                                     radno_mesto=radno_mesto, pozicija=pozicija)
        lekar.save()
        print("napravljen lekar " + ime)
        return redirect('index')
    else:
        niz = []
        for k in Klinika.objects.all():
            niz.extend([k.naziv])
        return render(request, 'registerLekara.html', {'niz': niz})


def registerAdmina(request):
    if request.method == 'POST':
        email_adresa = request.POST['email']
        lozinka = 'password'
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        broja_telefona = request.POST['btelefona']
        jedinstveni_broj_osiguranika = request.POST['jmbgnt']
        naziv_klinike = request.POST['radnomesto']

        if Admin.objects.filter(email_adresa=email_adresa).exists() or Pacijent.objects.filter(
                email_adresa=email_adresa).exists() or Lekar.objects.filter(email_adresa=email_adresa).exists():
            print("Email adresa je vec zauzeta")
            messages.info(request, "Email adresa je vec zauzeta")
            return redirect('registerLekara')

        elif "[" in ime or "]" in ime or "[NPL]" in ime:
            print("ime ne sme da sadrzi [NPL]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            return redirect('registerLekara')

        ime = "[NPL]" + ime

        admin = Admin.objects.create(email_adresa=email_adresa, lozinka=lozinka, ime=ime, prezime=prezime,
                                     broja_telefona=broja_telefona,
                                     jedinstveni_broj_osiguranika=jedinstveni_broj_osiguranika, datum=date.today(),
                                     naziv_klinike=naziv_klinike)
        admin.save()
        print("napravljen lekar " + ime)
        return redirect('loginKorisnik')
    else:
        niz = []
        for k in Klinika.objects.all():
            niz.extend([k.naziv])
        return render(request, 'registerAdmina.html', {'niz': niz})

def promeniLozinku(request):
    if request.method == 'POST':
        lozinka = request.POST['password']
        email_adresa = request.POST['email']
        if Lekar.objects.filter(email_adresa=email_adresa).exists():
            lekar = Lekar.objects.filter(email_adresa=email_adresa)[0]
            lekar.ime = lekar.ime.replace("[NPL]", "")
            lekar.lozinka = lozinka

            lekar.save()

            request.session['ime'] = Lekar.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime
            return redirect('index')

        elif Admin.objects.filter(email_adresa=email_adresa).exists():
            admin = Admin.objects.filter(email_adresa=email_adresa)[0]
            admin.ime = admin.ime.replace("[NPL]", "")
            admin.lozinka = lozinka

            admin.save()

            request.session['ime'] = Admin.objects.filter(email_adresa=email_adresa, lozinka=lozinka)[0].ime
            return redirect('index')
    else:
        return redirect('index')


def Omeni(request):
    if request.method == 'POST':
        email_adresa = ""
        uloga = ""

        if 'email' in request.session:
            email_adresa = request.session['email']
        if 'uloga' in request.session:
            uloga = request.session['uloga']

        if uloga == 'LEKAR':
            lozinka = Lekar.objects.filter(email_adresa=email_adresa)[0].lozinka
            ime = Lekar.objects.filter(email_adresa=email_adresa)[0].ime
            prezime = Lekar.objects.filter(email_adresa=email_adresa)[0].prezime
            broja_telefona = Lekar.objects.filter(email_adresa=email_adresa)[0].broja_telefona
            jedinstveni_broj_osiguranika = Lekar.objects.filter(email_adresa=email_adresa)[
                0].jedinstveni_broj_osiguranika
            datum = Lekar.objects.filter(email_adresa=email_adresa)[0].datum
            radno_mesto = Lekar.objects.filter(email_adresa=email_adresa)[0].radno_mesto
            pozicija = Lekar.objects.filter(email_adresa=email_adresa)[0].pozicija

            request.session['koga'] = email_adresa

            return render(request, 'omeni.html', {'email': email_adresa, 'uloga': uloga, 'ime': ime, 'prezime': prezime,
                                                  'lozinka': lozinka, 'broja_telefona': broja_telefona,
                                                  'jedinstveni_broj_osiguranika': jedinstveni_broj_osiguranika,
                                                  'datum': datum, 'radno_mesto': radno_mesto, 'pozicija': pozicija})
        elif uloga == 'ADMIN':
            lozinka = Admin.objects.filter(email_adresa=email_adresa)[0].lozinka
            ime = Admin.objects.filter(email_adresa=email_adresa)[0].ime
            prezime = Admin.objects.filter(email_adresa=email_adresa)[0].prezime
            broja_telefona = Admin.objects.filter(email_adresa=email_adresa)[0].broja_telefona
            jedinstveni_broj_osiguranika = Admin.objects.filter(email_adresa=email_adresa)[
                0].jedinstveni_broj_osiguranika
            datum = Admin.objects.filter(email_adresa=email_adresa)[0].datum
            radno_mesto = Admin.objects.filter(email_adresa=email_adresa)[0].radno_mesto
            pozicija = Admin.objects.filter(email_adresa=email_adresa)[0].pozicija

            request.session['koga'] = email_adresa

            return render(request, 'omeni.html', {'email': email_adresa, 'uloga': uloga, 'ime': ime, 'prezime': prezime,
                                                  'lozinka': lozinka, 'broja_telefona': broja_telefona,
                                                  'jedinstveni_broj_osiguranika': jedinstveni_broj_osiguranika,
                                                  'datum': datum, 'radno_mesto': radno_mesto, 'pozicija': pozicija})
        else:
            return redirect('index')


def IzmeniKorisnika(request):
    if request.method == 'POST':
        # email_adresa = request.POST['email'] #ne jos
        lozinka = request.POST['password']
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        broja_telefona = request.POST['broja_telefona']
        jedinstveni_broj_osiguranika = request.POST['jedinstveni_broj_osiguranika']

        if Lekar.objects.filter(email_adresa=request.session['email']).exists():
            lekar = Lekar.objects.filter(email_adresa=request.session['email'])[0]
            lekar.ime = ime
            lekar.lozinka = lozinka
            lekar.prezime = prezime
            lekar.broja_telefona = broja_telefona
            lekar.jedinstveni_broj_osiguranika = jedinstveni_broj_osiguranika

            lekar.save()

            # request.session['email'] = email_adresa
            request.session['ime'] = ime
            request.session['prezime'] = prezime

            return redirect('index')

        elif Admin.objects.filter(email_adresa=request.session['email']).exists():
            admin = Admin.objects.filter(email_adresa=request.session['email'])[0]
            admin.ime = ime
            admin.lozinka = lozinka
            admin.prezime = prezime
            admin.broja_telefona = broja_telefona
            admin.jedinstveni_broj_osiguranika = jedinstveni_broj_osiguranika

            admin.save()

            # request.session['email'] = email_adresa
            request.session['ime'] = ime
            request.session['prezime'] = prezime

            return redirect('index')

        return redirect('index')
    else:
        return redirect('index')


def pogledajPacijente(request):
    pacijenti = Pacijent.objects.all()
    return render(request, 'pogledajPacijente.html', {'pacijenti': pacijenti})


def PogledajPacijenta(request):
    odabrani = None
    for pacijent in Pacijent.objects.all():
        if request.POST[pacijent.ime] is not None:
            odabrani = pacijent
    return render(request, 'pogledajPacijenta.html', {'pacijent': odabrani})


def pogledajSale(request):
    uloga = ""
    prezime = ""
    if 'uloga' in request.session:
        uloga = request.session['uloga']

    sale = Sala.objects.all()
    return render(request, 'pogledajSale.html', {'sale': sale, 'uloga': uloga})


def pogledajSalu(request):
    odabrani = None
    for salaa in Sala.objects.all():
        try:
            if request.POST[salaa.naziv] is not None:
                odabrani = salaa
        except:
            pass
    if odabrani is not None:
        return render(request, 'pogledajSalu.html', {'sala': odabrani})


def IzmeniSalu(request):
    if request.method == 'POST':
        naziv = request.POST['naziv']
        opis = request.POST['opis']

        if Sala.objects.filter(naziv=naziv).exists():
            sala = Sala.objects.filter(naziv=naziv)[0]
            sala.opis = opis

            sala.save()

            return redirect('index')
        return redirect('index')
    else:
        return redirect('index')


def ObrisiSalu(request):
    try:
        Sala.objects.filter(naziv=request.POST['koga']).delete()
        return redirect('index')
    except:
        return redirect('index')


def DodajSalu(request):
    if request.method == 'POST':
        broj = request.POST['broj']
        naziv = request.POST['naziv']
        idd = request.POST['id']
        opis = request.POST['opis']

        if Sala.objects.filter(broj=broj).exists() or Sala.objects.filter(naziv=naziv).exists() or not \
                Klinika.objects.filter(naziv=idd).exists():
            messages.info(request, "_")
            return redirect('DodajSalu')
        while True:
            try:
                sala = Sala.objects.create(broj=broj, naziv=naziv, id_klinike_kojoj_pripada=idd, opis=opis)
                sala.save()
                storage = messages.get_messages(request)
                storage.used = True
                return redirect('index')
            except:
                pass
    else:
        niz = []
        for k in Klinika.objects.all():
            niz.extend([k.naziv])
        return render(request, 'dodajSalu.html', {'niz': niz})


def pogledajKlinike(request):
    uloga = ""
    if 'uloga' in request.session:
        uloga = request.session['uloga']

    kk = Klinika.objects.all()
    return render(request, 'pogledajKlinike.html', {'klinike': kk, 'uloga': uloga})


def pogledajKliniku(request):
    odabrani = None
    for kli in Klinika.objects.all():
        try:
            if request.POST[kli.naziv] is not None:
                odabrani = kli
        except:
            pass
    if odabrani is not None:
        return render(request, 'pogledajKliniku.html', {'klinika': odabrani})


def IzmeniKliniku(request):
    if request.method == 'POST':
        naziv = request.POST['naziv']
        opis = request.POST['opis']

        if Klinika.objects.filter(naziv=naziv).exists():
            k = Klinika.objects.filter(naziv=naziv)[0]
            k.opis = opis

            k.save()

            return redirect('index')
        return redirect('index')
    else:
        return redirect('index')


def pogledajLekare(request):
    kk = Lekar.objects.all()
    return render(request, 'pogledajLekare.html', {'lekari': kk})


def PogledajLekara(request):
    odabrani = None
    for kli in Lekar.objects.all():
        try:
            if request.POST[kli.ime] is not None:
                odabrani = kli
        except:
            pass
    if odabrani is not None:
        return render(request, 'pogledajLekara.html', {'lekar': odabrani})


def IzmeniLekara(request):
    if request.method == 'POST':
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        broja_telefona = request.POST['broja_telefona']

        if Lekar.objects.filter(ime=request.POST['koga']).exists():
            if request.session['ime'] == ime:
                request.session['ime'] = ime
                request.session['prezime'] = prezime

            k = Lekar.objects.filter(ime=request.POST['koga'])[0]
            k.ime = ime
            k.prezime = prezime
            k.broja_telefona = broja_telefona

            k.save()
            return redirect('index')
        return redirect('index')
    else:
        return redirect('index')


def ObrisiLekara(request):
    try:
        Lekar.objects.filter(ime=request.POST['koga']).delete()
        return redirect('index')
    except:
        return redirect('index')

#-----------------------------------------------------------------------------------------------------------------------
#nemoj ispod ove linije raditi

def registracijaPacijent(request):
    if request.method == 'POST':
        email_adresa = request.POST['email']
        lozinka = request.POST['sifra']
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        adresa_prebivalista = request.POST['adresa']
        grad = request.POST['grad']
        drzava = request.POST['drzava']
        broja_telefona = request.POST['broj']
        jedinstveni_broj_osiguranika = request.POST['jedinstveni']

        if Admin.objects.filter(email_adresa=email_adresa).exists() or Pacijent.objects.filter(
                email_adresa=email_adresa).exists() or Lekar.objects.filter(email_adresa=email_adresa).exists():
            # print("Email adresa je vec zauzeta")
            messages.info(request, "Email adresa je vec zauzeta")
            return redirect('registracijaPacijent')

        elif "[" in ime or "]" in ime or "[NPL]" in ime:
            # print("ime ne sme da sadrzi [NPL]")
            messages.info(request, "ime ne sme da sadrzi karaktere [ ili ]")
            return redirect('registracijaPacijent')

        pacijent = Pacijent.objects.create(email_adresa=email_adresa, lozinka=lozinka, ime=ime, prezime=prezime,
                                           broja_telefona=broja_telefona,
                                           jedinstveni_broj_osiguranika=jedinstveni_broj_osiguranika,
                                           adresa_prebivalista=adresa_prebivalista, grad=grad, drzava=drzava,
                                           sifra_bolesti="Prazno", datum=date.today().strftime("%d/%m/%Y"), diagnoza="Prazno", lekovi="Prazno",
                                           dioptrija="Prazno", alergije_na_lek="Prazno",
                                           visina="Prazno", tezina="Prazno", krvna_grupa="Prazno")
        pacijent.save()
        # print("napravljen pacijent " + ime)
        return redirect('loginPacijent')
    else:
        return render(request, 'pacijent/registracijaPacijent.html')

def loginPacijent(request):
    if request.method == 'POST':
        email_adresa = request.POST['email']
        sifra = request.POST['sifra']
        print("1")
        if Pacijent.objects.filter(email_adresa=email_adresa).exists():
            print("2")
            if Pacijent.objects.filter(lozinka=sifra).exists():
                print("3")
                request.session['email'] = email_adresa
                temp = list(Pacijent.objects.filter(email_adresa = email_adresa).values())
                recnik = temp[0]
                request.session['lozinka'] = sifra
                #ime = recnik.get('ime')
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
                request.session['lokacija'] = 0

                """email_adresa
                lozinka
                ime
                prezime
                adresa_prebivalista
                grad
                drzava
                broja_telefona
                jedinstveni_broj_osiguranika
                sifra_bolesti
                datum
                diagnoza
                lekovi
                dioptrija
                alergije_na_lek
                visina
                tezina
                krvna_grupa"""
                return render(request, 'pacijent/glavnaStranicaPacijent.html', {'email': request.session['email'], 'ime': request.session['ime'], 'prezime': request.session['prezime'],
                                                                                'lokacija': request.session['lokacija']})
            else:
                print("4")
                messages.info(request, "Sifra nije dobra!")
                return redirect('loginPacijent')
        else:
            print("5")
            messages.info(request, "Email koji ste uneli ne postoji!")
            return redirect('loginPacijent')
    else:
        pac = Pacijent.objects.all
        return render(request, 'pacijent/loginPacijent.html')

#return render(request, 'pogledajLekare.html', {'lekari': kk})

def glavnaStranicaPacijent(request):
    if request.method == 'POST':
        request.session['lokacija'] = 0
        return render(request, 'pacijent/glavnaStranicaPacijent.html', {'email': request.session['email'], 'ime': request.session['ime'], 'prezime': request.session['prezime'],
                                                                        'lokacija': request.session['lokacija']})
    else:
        request.session['lokacija'] = 0
        return render(request, 'pacijent/glavnaStranicaPacijent.html', {'email': request.session['email'], 'ime': request.session['ime'], 'prezime': request.session['prezime'],
                                                                        'lokacija': request.session['lokacija']})

def licniPodaciPacijent(request):
    if request.method == 'POST':
        request.session['lokacija'] = 1

        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'email': request.session['email'], 'ime': request.session['ime'], 'prezime': request.session['prezime'], 'lokacija': request.session['lokacija'],
                       'lozinka' : request.session['lozinka'], 'adresa' : request.session['adresa_prebivalista'], 'grad': request.session['grad'], 'drzava': request.session['drzava'],
                       'broj': request.session['broja_telefona'], 'jedinstven': request.session['jedinstveni_broj_osiguranika']})

    else:
        request.session['lokacija'] = 1
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'email': request.session['email'], 'ime': request.session['ime'],
                       'prezime': request.session['prezime'], 'lokacija': request.session['lokacija'],
                       'lozinka': request.session['lozinka'], 'adresa': request.session['adresa_prebivalista'],
                       'grad': request.session['grad'], 'drzava': request.session['drzava'],
                       'broj': request.session['broja_telefona'],
                       'jedinstven': request.session['jedinstveni_broj_osiguranika']})
#email_adresa = request.POST['email']
def promenaLicniPodaciPacijent(request):
    if request.method == 'POST':
        if(request.session['lokacija'] == 1):
            request.session['lokacija'] = 1.5
            return render(request, 'pacijent/glavnaStranicaPacijent.html',
                          {'email': request.session['email'], 'ime': request.session['ime'],
                           'prezime': request.session['prezime'], 'lokacija': request.session['lokacija'],
                           'lozinka': request.session['lozinka'], 'adresa': request.session['adresa_prebivalista'],
                           'grad': request.session['grad'], 'drzava': request.session['drzava'],
                           'broj': request.session['broja_telefona'],
                           'jedinstven': request.session['jedinstveni_broj_osiguranika']})
        else:
            request.session['lokacija'] = 1
            pacijent = Pacijent.objects.get(email_adresa = request.session['email'])
            if(request.POST.get('ime2', "")!=""):
                ime = request.POST['ime2']
                request.session['ime'] = ime
                pacijent.ime = ime
            if (request.POST.get('prezime2', "") != ""):
                prezime = request.POST['prezime2']
                request.session['prezime'] = prezime
                pacijent.prezime = prezime
            if (request.POST.get('lozinka2', "") != ""):
                lozinka = request.POST['lozinka2']
                request.session['lozinka'] = lozinka
                pacijent.lozinka = lozinka
            if (request.POST.get('adresa2', "") != ""):
                adresa_prebivalista = request.POST['adresa2']
                request.session['adresa_prebivalista'] = adresa_prebivalista
                pacijent.adresa_prebivalista = adresa_prebivalista
            if (request.POST.get('grad2', "") != ""):
                grad = request.POST['grad2']
                request.session['grad'] = grad
                pacijent.grad = grad
            if (request.POST.get('drzava2', "") != ""):
                drzava = request.POST['drzava2']
                request.session['drzava'] = drzava
                pacijent.drzava = drzava
            if (request.POST.get('broj2', "") != ""):
                broja_telefona = request.POST['broj2']
                request.session['broja_telefona'] = broja_telefona
                pacijent.broja_telefona = broja_telefona
            #request.POST.get('ime2', "")
            pacijent.save()
            return render(request, 'pacijent/glavnaStranicaPacijent.html',
                          {'email': request.session['email'], 'ime': request.session['ime'],
                           'prezime': request.session['prezime'], 'lokacija': request.session['lokacija'],
                           'lozinka': request.session['lozinka'], 'adresa': request.session['adresa_prebivalista'],
                           'grad': request.session['grad'], 'drzava': request.session['drzava'],
                           'broj': request.session['broja_telefona'],
                           'jedinstven': request.session['jedinstveni_broj_osiguranika']})
    else:
        #request.session['lokacija'] = 1.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'email': request.session['email'], 'ime': request.session['ime'],
                       'prezime': request.session['prezime'], 'lokacija': request.session['lokacija'],
                       'lozinka': request.session['lozinka'], 'adresa': request.session['adresa_prebivalista'],
                       'grad': request.session['grad'], 'drzava': request.session['drzava'],
                       'broj': request.session['broja_telefona'],
                       'jedinstven': request.session['jedinstveni_broj_osiguranika']})

def zdravstveniKartonPacijent(request):
    if request.method == 'POST':
        request.session['lokacija'] = 2
        pacijent = Pacijent.objects.get(email_adresa = request.session['email'])
        request.session['sifra_bolesti'] = pacijent.sifra_bolesti
        request.session['datum'] = pacijent.datum
        request.session['diagnoza'] = pacijent.diagnoza
        request.session['lekovi'] = pacijent.lekovi
        request.session['dioptrija'] = pacijent.dioptrija
        request.session['alergije_na_lek'] = pacijent.alergije_na_lek
        request.session['visina'] = pacijent.visina
        request.session['tezina'] = pacijent.tezina
        request.session['krvna_grupa'] = pacijent.krvna_grupa

        return render(request, 'pacijent/glavnaStranicaPacijent.html', {'ime':request.session['ime'],'prezime':request.session['prezime'],'jedinstven':request.session['jedinstveni_broj_osiguranika'],
                                                                       'sifra': request.session['sifra_bolesti'],'datum':request.session['datum'],'diagnoza':request.session['diagnoza'],
                                                                       'lekovi': request.session['lekovi'],'dioptrija':request.session['dioptrija'],'alergije':request.session['alergije_na_lek'],
                                                                       'visina': request.session['visina'],'tezina':request.session['tezina'],'krvna':request.session['krvna_grupa'],
                                                                        'lokacija': request.session['lokacija']
                                                                       })
    else:
        request.session['lokacija'] = 2
        pacijent = Pacijent.objects.get(email_adresa=request.session['email'])
        request.session['sifra_bolesti'] = pacijent.sifra_bolesti
        request.session['datum'] = pacijent.datum
        request.session['diagnoza'] = pacijent.diagnoza
        request.session['lekovi'] = pacijent.lekovi
        request.session['dioptrija'] = pacijent.dioptrija
        request.session['alergije_na_lek'] = pacijent.alergije_na_lek
        request.session['visina'] = pacijent.visina
        request.session['tezina'] = pacijent.tezina
        request.session['krvna_grupa'] = pacijent.krvna_grupa

        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'ime': request.session['ime'], 'prezime': request.session['prezime'],
                       'jedinstven': request.session['jedinstveni_broj_osiguranika'],
                       'sifra': request.session['sifra_bolesti'], 'datum': request.session['datum'],
                       'diagnoza': request.session['diagnoza'],
                       'lekovi': request.session['lekovi'], 'dioptrija': request.session['dioptrija'],
                       'alergije': request.session['alergije_na_lek'],
                       'visina': request.session['visina'], 'tezina': request.session['tezina'],
                       'krvna': request.session['krvna_grupa'],'lokacija': request.session['lokacija']
                       })

def prikazKlinikaPacijent(request):
    if request.method == 'POST':
        klinike = Klinika.objects.all()
        request.session['lokacija'] = 3
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'klinike': klinike})
    else:
        klinike = Klinika.objects.all()
        request.session['lokacija'] = 3
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'klinike': klinike})

def prikazKlinikaPacijentSortirano(request):
    if request.method == 'POST':
        temp = request.POST['sortiraj']
        if(temp == "Sortiraj po nazivu"):
            poCemu = "naziv"
        elif temp == "Sortiraj po adresi":
            poCemu = "adresa"
        else:
            poCemu = "opis"
        klinike = Klinika.objects.order_by(poCemu)
        request.session['lokacija'] = 3
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'klinike': klinike})
    else:
        temp = request.POST['sortiraj']
        if (temp == "Sortiraj po nazivu"):
            poCemu = "naziv"
        elif temp == "Sortiraj po adresi":
            poCemu = "adresa"
        else:
            poCemu = "opis"
        klinike = Klinika.objects.order_by(poCemu)
        request.session['lokacija'] = 3
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'klinike': klinike})

def prikazLekaraKlinikePacijent(request):
    if request.method == 'POST':
        nazivKlinike = request.POST['nazivKlinike']
        naziv = nazivKlinike.split()
        lekari = Lekar.objects.filter(radno_mesto = naziv[3])
        request.session['lokacija'] = 3.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'lekari': lekari})
    else:
        request.session['lokacija'] = 3.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija']})
