from calendar import monthrange
from time import strptime
from scripts.ucitajSkriptu import run
from clinic.models import Admin, Klinika, Odmor
from pacijent.models import Pacijent, Pregled, Operacije, TipPregleda
from django.contrib import messages
from datetime import date
from clinic.models import Lekar
from clinic.models import Sala
import datetime
import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from pacijent.tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.middleware import csrf
import time

pregledani = []


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

    radniKalendar = ''
    pacijenti = ''
    preg = ''
    try:
        preg = NapraviPregled(email)
        radniKalendar = NapraviRadniKalendar(email)
        pacijenti = NadjiPacijente(email, req)
    except:
        pass
    return render(req, 'index.html',
                  {'ime': ime, 'email': email, 'uloga': uloga, 'prezime': prezime, 'radniKalendar': radniKalendar,
                   'pacijenti': pacijenti, 'preg': preg})


def IzlogujSe(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    ime = ""  # ako ne postoji
    email = ""
    uloga = ""
    request.session['ime'] = ''
    request.session['email'] = ''
    request.session['uloga'] = 'NEULOGOVAN'
    del request.session['ulogovan']
    return render(request, 'index.html', {'ime': ime, 'email': email, 'uloga': uloga})


def register_clinic_admin(req):
    if 'uloga' not in req.session or req.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    return render(req, 'superadmin/register.html')


# def registracija_pacijent(req):
#   return render(req, 'pacijent/registracija.html')

# def login_pacijent2(req):
#   return  render(req, 'pacijent/login.html')


def login_pacijent(req):
    return render(req, 'login.html')


def izmeni_lekara(req):
    if 'uloga' not in req.session or req.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    return render(req, 'lekar/izmeniInformacijeLekara.html')


def izmeni_kliniku(req):
    if 'uloga' not in req.session or req.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    return render(req, 'klinika/izmeniInformacijeKlinike.html')


def izmeni_salu(req):
    if 'uloga' not in req.session or req.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    return render(req, 'sala/izmeniInformacijeSale.html')


######################################################################################


def registerLekara(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        email_adresa = request.POST['email']
        lozinka = 'password'
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        broja_telefona = request.POST['btelefona']
        jedinstveni_broj_osiguranika = request.POST['jmbgnt']
        radno_mesto = request.POST['radnomesto']
        pozicija = request.POST['pozicija']
        smena = request.POST['smena']

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
                                     radno_mesto=radno_mesto, pozicija=pozicija, smena=smena)
        lekar.save()
        print("napravljen lekar " + ime)
        return redirect('index')
    else:
        niz = []
        for k in Klinika.objects.all():
            niz.extend([k.naziv])
        return render(request, 'registerLekara.html', {'niz': niz})


def registerAdmina(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
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
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
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
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
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
            radno_mesto = Admin.objects.filter(email_adresa=email_adresa)[0].naziv_klinike

            request.session['koga'] = email_adresa

            return render(request, 'omeni.html', {'email': email_adresa, 'uloga': uloga, 'ime': ime, 'prezime': prezime,
                                                  'lozinka': lozinka, 'broja_telefona': broja_telefona,
                                                  'jedinstveni_broj_osiguranika': jedinstveni_broj_osiguranika,
                                                  'datum': datum, 'radno_mesto': radno_mesto})
        else:
            return redirect('index')


def IzmeniKorisnika(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        # email_adresa = request.POST['email'] #ne jos
        lozinka = request.POST['password']
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        broja_telefona = request.POST['broja_telefona']
        jedinstveni_broj_osiguranika = request.POST['jedinstveni_broj_osiguranika']
        smena = request.POST['smena']

        if Lekar.objects.filter(email_adresa=request.session['email']).exists():
            lekar = Lekar.objects.filter(email_adresa=request.session['email'])[0]
            lekar.ime = ime
            lekar.lozinka = lozinka
            lekar.prezime = prezime
            lekar.broja_telefona = broja_telefona
            lekar.jedinstveni_broj_osiguranika = jedinstveni_broj_osiguranika
            lekar.smena = smena

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
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    pacijenti = Pacijent.objects.all()
    return render(request, 'pogledajPacijente.html', {'pacijenti': pacijenti})


def PogledajPacijenta(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')

    for pacijent in Pacijent.objects.all():
        try:
            if request.POST[pacijent.email_adresa] is not None:
                odabrani = pacijent
                cwmp = cwmpf(pacijent, request)
                if cwmp == 'da':
                    print("DIE CIS SCUM")
                print("WHOMSTDV DONE DID THIS")
                return render(request, 'pogledajPacijenta.html', {'pacijent': odabrani, 'cwmp': cwmp})
        except:
            pass


def cwmpf(pacijent, request):
    try:
        print("--------//----------//---------//----------//-------")
        pacijenti = []
        pp = Pregled.objects.filter(lekar=request.session['email'])
        print("nas p je " + str(pacijent))
        for p in pp:
            if p.zakazan != 'Prazno':
                print("br " + str(p.zakazan))
                pacijenti.extend([p.zakazan])

        print(str(pacijenti))

        if str(pacijent).strip() in pacijenti:
            return 'da'
        return 'ne'
    except:
        return 'ne'


def PPregledaj(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if True:#try:
        pacijent = Pacijent.objects.filter(email_adresa=request.POST['koga'])[0]

        print("llllllllllllllllllllllllllllllllllllllllllllllllllll")
        print(request.POST['koga'])
        print(pacijent.email_adresa)

        vreme = datetime.datetime.now()
        sala = "[Prazno]"

        tip_pregleda = "Opsti Pregled"
        id = 0
        while Pregled.objects.filter(id=id).exists():
            id += 1
        ii = 0
        while True:
            ii += 1
            if ii >= 1000:
                return HttpResponse('<h1>Error 400</h1>Bad request', status=400)
            if True:#try:
                email = ""
                if 'email' in request.session:
                    email = request.session['email']
                klinika = ""
                for korinisk in Lekar.objects.all():
                    if korinisk.email_adresa == email:
                        klinika = korinisk.radno_mesto
                for korinisk in Admin.objects.all():
                    if korinisk.email_adresa == email:
                        klinika = korinisk.naziv_klinike

                ter = Pregled.objects.create(id=id, klinika=klinika, zakazan=request.POST['koga'], lekar=email,
                                                         sala=sala,
                                                         tip_pregleda=tip_pregleda, vreme=vreme.__str__().split(".")[0],
                                                         sifra_bolesti="Prazno",
                                                         diagnoza="Prazno", lekovi="Prazno", prihvacen="da",
                                                         ocenaLekara=-1,
                                                         ocenaKlinike=-1)
                ter.save()
                storage = messages.get_messages(request)
                storage.used = True

                return render(request, 'pregledaj.html',
                                    {'pregled': ter, 'pacijent': pacijent, 'email': email})

    '''        except:
                return HttpResponse('<h1>Error 400</h1>Bad request<br />Doslo je do greske', status=400)
    except:
        return HttpResponse('<h1>Error 400</h1>Bad request<br />Doslo je do greske', status=400)'''


def pogledajSale(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    uloga = ""
    if 'uloga' in request.session:
        uloga = request.session['uloga']
    kk = Pregled.objects.all()
    sale = Sala.objects.all()
    mapa = napraviMapuTerminaSala(kk, sale)
    return render(request, 'pogledajSale.html', {'sale': sale, 'uloga': uloga, 'mapa': mapa})


def pogledajSalu(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
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
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        naziv = request.POST['koga']
        opis = request.POST['opis']
        broj = request.POST['broj']
        novNaziv = request.POST['naziv']

        if Pregled.objects.filter(sala=naziv,
                                  vreme__range=[date.today(), date.today() + datetime.timedelta(days=1000)]).exists():
            return HttpResponse('<h1>Error 400</h1>Bad request<br />Postoje zakazani termini u ovoj sali', status=400)
        if Sala.objects.filter(naziv=naziv).exists():
            sala = Sala.objects.filter(naziv=naziv)[0]
            sala.opis = opis
            if not Sala.objects.filter(broj=broj).exists():
                sala.broj = broj
            if not Sala.objects.filter(naziv=novNaziv).exists():
                sala.naziv = novNaziv

                for pregd in Pregled.objects.filter(sala=naziv):  # za stare zakazane termine
                    pregd.sala = novNaziv
                    pregd.save()

            sala.save()

            return redirect('index')
        return redirect('index')
    else:
        return redirect('index')


def ObrisiSalu(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if Pregled.objects.filter(sala=request.POST['koga'],
                              vreme__range=[date.today(), date.today() + datetime.timedelta(days=1000)]).exists():
        return HttpResponse('<h1>Error 400</h1>Bad request<br />Postoje zakazani termini u ovoj sali', status=400)
    try:
        Sala.objects.filter(naziv=request.POST['koga']).delete()
        return redirect('index')
    except:
        return redirect('index')


def DodajSalu(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
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
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    uloga = ""
    if 'uloga' in request.session:
        uloga = request.session['uloga']

    kk = Klinika.objects.all()
    return render(request, 'pogledajKlinike.html', {'klinike': kk, 'uloga': uloga})


def pogledajKliniku(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
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
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        nazivog = request.POST['nazivog']
        naziv = request.POST['naziv']
        adresa = request.POST['adresa']
        opis = request.POST['opis']

        if Klinika.objects.filter(naziv=naziv).exists() and naziv != nazivog:
            print("Ime klinike je vec zauzeto")
            messages.info(request, "Ime klinike je vec zauzeto")
            return redirect('IzmeniKliniku')

        elif Klinika.objects.filter(naziv=nazivog).exists():
            k = Klinika.objects.filter(naziv=nazivog)[0]
            if naziv != "":
                k.naziv = naziv

                for ss in Sala.objects.filter(id_klinike_kojoj_pripada=nazivog):
                    ss.id_klinike_kojoj_pripada = naziv
                    ss.save()

                for pp in Pregled.objects.filter(klinika=nazivog):
                    pp.klinika = naziv
                    pp.save()

                for oo in Operacije.objects.filter(klinika=nazivog):
                    oo.klinika = naziv
                    oo.save()

                for oo in Odmor.objects.filter(klinika=nazivog):
                    oo.klinika = naziv
                    oo.save()

                for ll in Lekar.objects.filter(radno_mesto=nazivog):
                    ll.radno_mesto = naziv
                    ll.save()

                for aa in Admin.objects.filter(naziv_klinike=nazivog):
                    aa.naziv_klinike = naziv
                    aa.save()

            k.adresa = adresa
            k.opis = opis
            k.save()

            return redirect('index')
        return redirect('index')
    else:
        return redirect('index')


def pogledajLekare(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    kk = Lekar.objects.all()
    return render(request, 'pogledajLekare.html', {'lekari': kk})


def PogledajLekara(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    odabrani = None
    for kli in Lekar.objects.all():
        try:
            if request.POST[kli.email_adresa] is not None:
                odabrani = kli
        except:
            pass
    if odabrani is not None:
        return render(request, 'pogledajLekara.html', {'lekar': odabrani})


def IzmeniLekara(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        broja_telefona = request.POST['broja_telefona']

        if Lekar.objects.filter(email_adresa=request.POST['koga']).exists():
            if request.session['ime'] == ime:
                request.session['ime'] = ime
                request.session['prezime'] = prezime

            k = Lekar.objects.filter(email_adresa=request.POST['koga'])[0]
            k.ime = ime
            k.prezime = prezime
            k.broja_telefona = broja_telefona

            nijeZakazano = True

            for pregled in Pregled.objects.filter(lekar=request.POST['koga']):
                if pregled.vreme >= datetime.datetime.now():
                    nijeZakazano = False

            if nijeZakazano:
                k.save()
                return redirect('index')
            else:
                return HttpResponse('<h1>Error 400</h1>Bad request<br />Postoje zakazani termini ovog tipa pregleda',
                                    status=400)
        return redirect('index')
    else:
        return redirect('index')


def ObrisiLekara(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    try:
        nijeZakazano = True

        for pregled in Pregled.objects.filter(lekar=request.POST['koga']):
            if pregled.vreme >= datetime.datetime.now():
                nijeZakazano = False

        if nijeZakazano:
            Lekar.objects.filter(email_adresa=request.POST['koga']).delete()
            return redirect('index')
        else:
            return HttpResponse('<h1>Error 400</h1>Bad request<br />Lekar ima aktivne preglede',
                                status=400)
    except:
        return redirect('index')


def PogledajTermine(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    uloga = ""
    if 'uloga' in request.session:
        uloga = request.session['uloga']
    email = ""
    if 'email' in request.session:
        email = request.session['email']
    klinika = ""
    for korinisk in Lekar.objects.all():
        if korinisk.email_adresa == email:
            klinika = korinisk.klinika
    for korinisk in Admin.objects.all():
        if korinisk.email_adresa == email:
            klinika = korinisk.naziv_klinike
    autoTermin(request)
    sale = []
    print("sale za " + klinika)
    for sala in Sala.objects.all():
        if sala.id_klinike_kojoj_pripada == klinika:
            sale.append(sala)
            print(sala)

    enddate = date.today() + datetime.timedelta(days=6)
    kk = Pregled.objects.filter(vreme__range=[date.today(), enddate], klinika=klinika)
    mapa = napraviMapu(kk, sale)
    return render(request, 'pogledajTermine.html', {'termini': kk, 'uloga': uloga, 'mapa': mapa})


def PogledajTermin(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    uloga = ""
    if 'uloga' in request.session:
        uloga = request.session['uloga']

    odabrani = Pregled.objects.filter(id=request.POST['koga'])[0]
    kk = Pregled.objects.filter(vreme__range=[odabrani.vreme.date(), odabrani.vreme + datetime.timedelta(days=1)])

    email = ""
    if 'email' in request.session:
        email = request.session['email']
    klinika = ""
    for korinisk in Lekar.objects.all():
        if korinisk.email_adresa == email:
            klinika = korinisk.klinika
    for korinisk in Admin.objects.all():
        if korinisk.email_adresa == email:
            klinika = korinisk.naziv_klinike

    sale = []
    for sala in Sala.objects.all():
        if sala.id_klinike_kojoj_pripada == klinika:
            sale.append(sala)
            print(sala)
    mapa = napraviMapu2(kk, sale)

    lekari = Lekar.objects.filter(radno_mesto=klinika)
    sale = Sala.objects.filter(id_klinike_kojoj_pripada=klinika)

    lekar = Lekar.objects.filter(radno_mesto=klinika, email_adresa=odabrani.lekar)[0]
    sala = None
    try:
        sala = Sala.objects.filter(id_klinike_kojoj_pripada=klinika, naziv=odabrani.sala)[0]
    except:
        try:
            idd = odabrani.sala.split('-')
            sala = Sala.objects.filter(id_klinike_kojoj_pripada=klinika, id=idd[0])[0]
        except:
            pass

    lekarid = 0
    salaid = 0
    ii = 0
    for le in lekari:
        if le.email_adresa == lekar.email_adresa:
            lekarid = ii
            break
        ii += 1

    try:
        ii = 0
        for le in sale:
            if le.naziv == sala.naziv:
                salaid = ii
                break
            ii += 1
    except:
        salaid = -1

    return render(request, 'pogledajTermin.html',
                  {'mapa': mapa, 'lekari': lekari, 'sale': sale, 'lekar': lekarid, 'sala': salaid,
                   'termin': Pregled.objects.filter(id=odabrani.id)[0]})


def ObrisiTermin(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    try:
        Pregled.objects.filter(id=request.POST['koga']).delete()
        return redirect('index')
    except:
        return redirect('index')


def IzmeniTermin(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        id = request.POST['broj']
        lekar = request.POST['lekar']
        sala = request.POST['sala']
        vreme = request.POST['vreme']

        if Pregled.objects.filter(id=id).exists():
            k = Pregled.objects.filter(id=id)[0]

            if Lekar.objects.filter(email_adresa=lekar).exists():
                k.lekar = Lekar.objects.filter(email_adresa=lekar)[0].email_adresa

            if Sala.objects.filter(broj=sala).exists():
                k.sala = Sala.objects.filter(broj=sala)[0].naziv

            k.vreme = vreme
            if proveriTermin(vreme, k.sala, k.lekar, id):
                print("sacuvano")
                k.save()
                return redirect('index')
            return HttpResponse('<h1>Error 400</h1>Bad request<br />Datumi se ne poklapaju', status=400)
    else:
        return HttpResponse('<h1>Error 400</h1>Bad request<br />GET metoda nije podrzana', status=400)


def DodajTermin(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    try:
        if request.method == 'POST':
            id = request.POST['broj']
            lekar = request.POST['lekar']
            sala = request.POST['sala']
            vreme = request.POST['vreme']
            tip_pregleda = request.POST['tip_pregleda']
            print(lekar)
            if not Pregled.objects.filter(id=id).exists():
                if proveriTermin(vreme, sala, lekar):
                    ii = 0
                    while True:
                        ii += 1
                        if ii >= 1000:
                            return HttpResponse('<h1>Error 400</h1>Bad request', status=400)
                        try:
                            email = ""
                            if 'email' in request.session:
                                email = request.session['email']
                            klinika = ""
                            for korinisk in Lekar.objects.all():
                                if korinisk.email_adresa == email:
                                    klinika = korinisk.radno_mesto
                            for korinisk in Admin.objects.all():
                                if korinisk.email_adresa == email:
                                    klinika = korinisk.naziv_klinike
                            print("pravim......")
                            # ter = Pregled.objects.create(id=id, klinika=klinika, zakazan="Prazno", lekar=lekar,
                            #                             sala=sala, tip_pregleda=tip_pregleda,
                            #                             vreme=vreme.__str__().split(".")[0],
                            #                             sifra_bolesti="Prazno", diagnoza="Prazno", lekovi="Prazno",
                            #                             prihvacen='da', ocenalekara=-1, ocenaklinike=-1, temp='da')
                            ter = Pregled.objects.create(id=id, klinika=klinika, zakazan="Prazno", lekar=lekar,
                                                         sala=sala,
                                                         tip_pregleda=tip_pregleda, vreme=vreme.__str__().split(".")[0],
                                                         sifra_bolesti="Prazno",
                                                         diagnoza="Prazno", lekovi="Prazno", prihvacen="da",
                                                         ocenaLekara=-1,
                                                         ocenaKlinike=-1)
                            print("napravio......")
                            ter.save()
                            print("sacuvao......")
                            storage = messages.get_messages(request)
                            storage.used = True
                            return redirect('index')
                        except:
                            return HttpResponse('<h1>Error 400</h1>Bad request<br />Datumi se ne poklapaju', status=400)
                else:
                    return HttpResponse('<h1>Error 400</h1>Bad request<br />Datumi se ne poklapaju', status=400)
            return HttpResponse('<h1>Error 400</h1>Bad request<br />ID je vec zauzet', status=400)
        else:
            email = ""
            if 'email' in request.session:
                email = request.session['email']
            uloga = ""
            if 'uloga' in request.session:
                uloga = request.session['uloga']
            klinika = ""
            for korinisk in Lekar.objects.all():
                if korinisk.email_adresa == email:
                    klinika = korinisk.radno_mesto
            for korinisk in Admin.objects.all():
                if korinisk.email_adresa == email:
                    klinika = korinisk.naziv_klinike
            sale = []
            for sala in Sala.objects.all():
                if sala.id_klinike_kojoj_pripada == klinika:
                    sale.append(sala)
                    print(sala)
            kk = Pregled.objects.filter(
                vreme__range=[date.today(), date.today() + datetime.timedelta(days=1)])
            mapa = napraviMapu2(kk, sale)

            lekari = Lekar.objects.filter(radno_mesto=klinika)
            sale = Sala.objects.filter(id_klinike_kojoj_pripada=klinika)
            return render(request, "dodajTermin.html",
                          {'klinika': klinika, 'mapa': mapa, 'lekari': lekari, 'sale': sale, 'uloga': uloga,
                           'lekar': email, 'vreme': date.today(), 'tip': TipPregleda.objects.all()})
    except:
        return HttpResponse('<h1>Error 400</h1>Bad request', status=400)


def proveriTermin(vreme, sala, lekar, idd=-9999):
    try:
        for termin in Pregled.objects.all():
            if termin.sala == sala and termin.id != idd:
                if not (termin.vreme > vreme + datetime.timedelta(minutes=30) or termin.vreme + datetime.timedelta(
                        minutes=30) < vreme):
                    return False
        for termin in Pregled.objects.all():
            if termin.lekar == lekar and termin.id != idd:
                if not (termin.vreme > vreme + datetime.timedelta(minutes=30) or termin.vreme + datetime.timedelta(
                        minutes=30) < vreme):
                    return False
        lekarOBJ = None
        for lekarr in Pregled.objects.all():
            if lekarr.email_adresa == lekar:
                lekarOBJ = lekarr
                break

        for odmor in Odmor.objects.all():
            if odmor.lekar == lekarOBJ.email_adresa:
                if not (odmor.vreme > vreme + datetime.timedelta(minutes=30) or odmor.vreme + datetime.timedelta(
                        days=odmor.duzina) < vreme):
                    return False
        return True
    except:
        print('vreme')
        vreme = datetime.datetime.strptime(vreme, "%Y-%m-%d %H:%M:%S")
        print('vreme?')
        for termin in Pregled.objects.all():
            if termin.sala == sala and termin.id != idd:
                if not (termin.vreme > vreme + datetime.timedelta(minutes=30) or termin.vreme + datetime.timedelta(
                        minutes=30) < vreme):
                    return False
        for termin in Pregled.objects.all():
            if termin.lekar == lekar and termin.id != idd:
                if not (termin.vreme > vreme + datetime.timedelta(minutes=30) or termin.vreme + datetime.timedelta(
                        minutes=30) < vreme):
                    return False
        lekarOBJ = None
        for lekarr in Lekar.objects.all():
            if lekarr.email_adresa == lekar:
                lekarOBJ = lekarr
                break

        for odmor in Odmor.objects.all():
            if odmor.lekar == lekarOBJ.email_adresa:
                if not (odmor.vreme > vreme + datetime.timedelta(minutes=30) or odmor.vreme + datetime.timedelta(
                        days=odmor.duzina) < vreme):
                    return False
        return True


def proveriTermin2(vreme, sala, trajanje):
    try:
        for termin in Pregled.objects.all():
            if termin.sala == sala:
                if not (termin.vreme > vreme + datetime.timedelta(
                        minutes=trajanje) or termin.vreme + datetime.timedelta(
                        minutes=trajanje) < vreme):
                    return False
        return True
    except:
        print('vreme')
        vreme = datetime.datetime.strptime(vreme, "%Y-%m-%d %H:%M:%S")
        print('vreme?')
        for termin in Pregled.objects.all():
            if termin.sala == sala:
                if not (termin.vreme > vreme + datetime.timedelta(
                        minutes=trajanje) or termin.vreme + datetime.timedelta(
                        minutes=trajanje) < vreme):
                    return False
        return True


def napraviMapu(pregledi, sale):
    rezultat = ""
    for sala in sale:
        trenutni = datetime.time(0, 0, 0)
        rezultat += "<div style:\"display: inline;\">Za salu br " + sala.broj + " (\"<i>" + sala.naziv + "<i/>\") : "
        kraj = "<div style=\"background-color:green;padding: 5px;display: inline\">" + trenutni.__str__() + "</div>"
        pregledi = pregledi.order_by('vreme')
        for pregled in pregledi:
            if pregled.vreme.date() == datetime.datetime.now().date() and pregled.sala == sala.naziv:
                if pregled.vreme.time() > trenutni:
                    rezultat += kraj + "<div style=\"background-color:green;padding: 5px;display: inline\">-  " + pregled.vreme.time().__str__() + "</div>" + "<div style=\"background-color:red;padding: 5px;display: inline\">" + pregled.vreme.time().__str__() + "  -</div>"
                    trenutni = (pregled.vreme + datetime.timedelta(minutes=30)).time()
                    kraj = "<div style=\"background-color:red;padding: 5px;display: inline\">" + trenutni.__str__() + "</div>" + "<div style=\"background-color:green;padding: 5px;display: inline\">" + trenutni.__str__() + "</div>"
                else:
                    if pregled.vreme == datetime.time(0, 0, 0):
                        rezultat += "<div style:\"display: inline;\"><div style=\"background-color:red;padding: 5px;display: inline\">" + trenutni.__str__() + "</div>"
                    rezultat += "<div style=\"background-color:red;padding: 5px;display: inline\">" + (
                            pregled.vreme + datetime.timedelta(
                        minutes=30)).time().__str__() + "</div>" + "<div style=\"background-color:green;padding: 5px;display: inline\">" + (
                                        pregled.vreme + datetime.timedelta(minutes=30)).time().__str__() + "</div>"
                    trenutni = (pregled.vreme + datetime.timedelta(minutes=30)).time()
                    kraj = ""
        rezultat += kraj
        rezultat += "<div style=\"background-color:green;padding: 5px;display: inline\">- 24:00:00</div>"
        rezultat += "</div><br />"
    return rezultat


def napraviMapuTerminaSala(pregledi, sale):
    rezultatov = "var termini = ["
    for pregled2 in pregledi:
        print(pregled2.vreme)
        rezultat = ""
        for sala in sale:
            trenutni = datetime.time(0, 0, 0)
            rezultat += "<div style:\"display: inline;\">Za salu br " + sala.broj + " (\"<i>" + sala.naziv + "<i/>\") : "
            kraj = "<div style=\"background-color:green;padding: 5px;display: inline\">" + trenutni.__str__() + "</div>"
            pregledi = pregledi.order_by('vreme')
            for pregled in pregledi:

                if pregled.vreme.date() == pregled2.vreme.date() and pregled.sala == sala.naziv:
                    if pregled.vreme.time() > trenutni:
                        rezultat += kraj + "<div style=\"background-color:green;padding: 5px;display: inline\">-  " + pregled.vreme.time().__str__() + "</div>" + "<div style=\"background-color:red;padding: 5px;display: inline\">" + pregled.vreme.time().__str__() + "  -</div>"
                        trenutni = (pregled.vreme + datetime.timedelta(minutes=30)).time()
                        kraj = "<div style=\"background-color:red;padding: 5px;display: inline\">" + trenutni.__str__() + "</div>" + "<div style=\"background-color:green;padding: 5px;display: inline\">" + trenutni.__str__() + "</div>"
                    else:
                        if pregled.vreme == datetime.time(0, 0, 0):
                            rezultat += "<div style:\"display: inline;\"><div style=\"background-color:red;padding: 5px;display: inline\">" + trenutni.__str__() + "</div>"
                        rezultat += "<div style=\"background-color:red;padding: 5px;display: inline\">" + (
                                pregled.vreme + datetime.timedelta(
                            minutes=30)).time().__str__() + "</div>" + "<div style=\"background-color:green;padding: 5px;display: inline\">" + (
                                            pregled.vreme + datetime.timedelta(minutes=30)).time().__str__() + "</div>"
                        trenutni = (pregled.vreme + datetime.timedelta(minutes=30)).time()
                        kraj = ""
            rezultat += kraj
            rezultat += "<div style=\"background-color:green;padding: 5px;display: inline\">- 24:00:00</div>"
            rezultat += "</div><br />"
        if "[" + str(time.mktime(
                datetime.datetime.strptime(pregled2.vreme.strftime("%d/%m/%Y"), "%d/%m/%Y").timetuple())).split(".")[
            0] + ", '" + rezultat + "']," not in rezultatov:
            rezultatov += "[" + str(time.mktime(
                datetime.datetime.strptime(pregled2.vreme.strftime("%d/%m/%Y"), "%d/%m/%Y").timetuple())).split(".")[
                0] + ", '" + rezultat + "'],"

    deffa = ""

    for sala in sale:
        deffa += "<div style:\"display: inline;\">Za salu br " + sala.broj + " (\"<i>" + sala.naziv + "<i/>\") : "
        deffa += "<div style=\"background-color:green;padding: 5px;display: inline\">00:00:00 - 24:00:00</div>"
        deffa += "</div><br />"

    return rezultatov + "[-1,'" + deffa + "']]"


def napraviMapu2(pregledi, sale):
    rez = "var niz = ["
    pregledi = pregledi.order_by('vreme')
    for sala in sale:
        trenutni = datetime.time(0, 0, 0)
        rezultat = ""
        kraj = trenutni.__str__()

        for pregled in pregledi:
            if pregled.sala == sala.naziv:
                if pregled.vreme.date() == datetime.datetime.now().date():
                    if pregled.vreme.time() > trenutni:
                        rezultat += kraj + " - " + pregled.vreme.time().__str__() + ", "
                        trenutni = (pregled.vreme + datetime.timedelta(minutes=30)).time()
                        kraj = trenutni.__str__()
                    elif pregled.vreme.time() <= trenutni:
                        rezultat += (pregled.vreme + datetime.timedelta(minutes=30)).time().__str__()
                        trenutni = (pregled.vreme + datetime.timedelta(minutes=30)).time()
                        kraj = ""
        rezultat += kraj + " - 24:00:00"
        rez += "\"" + rezultat + "\","
    return rez[:-1] + "]"


def autoTermin(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    for klinika in Klinika.objects.all():
        kk = Pregled.objects.filter(vreme__range=[date.today(), date.today() + datetime.timedelta(days=1)],
                                    klinika=klinika.naziv)
        if len(kk) == 0:
            for i in (6, 8, 10, 12, 14, 16, 18, 20):
                try:
                    print("-------------------" + i.__str__())
                    sala = random.choice(Sala.objects.filter(id_klinike_kojoj_pripada=klinika.naziv))
                    print(sala)
                    lekar = random.choice(Lekar.objects.filter(radno_mesto=klinika.naziv))
                    print(lekar)
                    vreme = datetime.datetime.now().replace(hour=i, minute=0, second=0)

                    print(vreme.__str__())

                    manualTermin(lekar.email_adresa, sala.naziv, vreme, klinika.naziv, "Opsti Pregled", request)
                except:
                    print("nesto fali")
                    pass


def manualTermin(lekar, sala, vreme, klinika, tip_pregleda, request):
    id = 1
    if Pregled.objects.filter(id=id).exists():
        while Pregled.objects.filter(id=id).exists():
            id += 1

    if not Pregled.objects.filter(id=id).exists():
        if proveriTermin(vreme.__str__().split(".")[0], sala, lekar):
            ii = 0
            while True:
                ii += 1
                if ii >= 100:
                    return
                try:
                    cena = 0

                    if not TipPregleda.objects.filter(id=tip_pregleda).exists():
                        if tip_pregleda == 'Opsti Pregled':
                            tpp = TipPregleda.objects.create(id=tip_pregleda, ime='Opsti Pregled', cena=1500,
                                                             trajanje=15)
                            tpp.save()
                        else:
                            pass

                    pregled = TipPregleda.objects.filter(id=tip_pregleda)[0]

                    cena = pregled.cena
                    print(cena)

                    ter = Pregled.objects.create(id=id, klinika=klinika, zakazan="Prazno", lekar=lekar, sala=sala,
                                                 tip_pregleda=tip_pregleda, vreme=vreme.__str__().split(".")[0],
                                                 sifra_bolesti="Prazno",
                                                 diagnoza="Prazno", lekovi="Prazno", prihvacen="da", ocenaLekara=-1,
                                                 ocenaKlinike=-1)

                    ter.save()

                    return
                except:
                    pass


def manualTerminLekar(lekar, sala, vreme, klinika, tip_pregleda, zakazan):
    id = 1
    if Pregled.objects.filter(id=id).exists():
        while Pregled.objects.filter(id=id).exists():
            id += 1

    if not Pregled.objects.filter(id=id).exists():
        if proveriTermin(vreme.__str__().split(".")[0], sala, lekar):
            ii = 0
            while True:
                ii += 1
                if ii >= 100:
                    return
                try:
                    cena = 0

                    if not TipPregleda.objects.filter(id=tip_pregleda).exists():
                        if tip_pregleda == 'Opsti Pregled':
                            tpp = TipPregleda.objects.create(id=tip_pregleda, ime='Opsti Pregled', cena=1500,
                                                             trajanje=15)
                            tpp.save()
                        else:
                            pass

                    pregled = TipPregleda.objects.filter(id=tip_pregleda)[0]

                    cena = pregled.cena
                    print(cena)
                    print("zakazan " + zakazan)
                    ter = Pregled.objects.create(id=id, klinika=klinika, zakazan=zakazan, lekar=lekar, sala="Prazno",
                                                 tip_pregleda=tip_pregleda, vreme=vreme.__str__().split(".")[0],
                                                 sifra_bolesti="Prazno",
                                                 diagnoza="Prazno", lekovi="Prazno", prihvacen="ne", ocenaLekara=-1,
                                                 ocenaKlinike=-1)

                    ter.save()

                    return
                except:
                    pass


def DodajOdmor(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        vreme = request.POST['vreme']
        duzina = request.POST['duzina']
        lekar = request.POST['koga']
        idd = 0

        bdate = datetime.datetime.now()
        bdate = bdate.replace(minute=0, hour=0, second=0, year=date.today().year, month=1, day=1)
        enddate = bdate.replace(minute=0, hour=0, second=0, year=date.today().year + 1, month=1, day=1)

        if Odmor.objects.filter(lekar=lekar, vreme__range=[bdate, enddate]).exists():
            return redirect('index')

        for lek in Lekar.objects.all():
            if lek.email_adresa == lekar:
                lekar = lek

        while True:
            if idd > 100:
                return HttpResponse('<h1>Error 400</h1>Bad request', status=400)
            try:
                odmor = Odmor.objects.create(id=idd, klinika=lekar.radno_mesto, lekar=lekar.email_adresa,
                                             vreme=vreme.__str__().split(".")[0],
                                             duzina=duzina, aktiviran=0)
                odmor.save()
                storage = messages.get_messages(request)
                storage.used = True
                return redirect('index')
            except:
                pass
    else:
        niz = []
        for k in Odmor.objects.all():
            niz.extend([k])
        email_adresa = ""
        uloga = ""

        if 'email' in request.session:
            email_adresa = request.session['email']
        if 'uloga' in request.session:
            uloga = request.session['uloga']

        if uloga == 'LEKAR':
            request.session['koga'] = email_adresa
            bdate = datetime.datetime.now()
            bdate = bdate.replace(minute=0, hour=0, second=0, year=date.today().year, month=1, day=1)
            enddate = bdate.replace(minute=0, hour=0, second=0, year=date.today().year + 1, month=1, day=1)
            odobreno = not Odmor.objects.filter(lekar=email_adresa, vreme__range=[bdate, enddate]).exists()
            vreme = datetime.datetime.now()
            vreme = vreme.replace(minute=0, hour=0, second=0)
            return render(request, 'zakaziOdmor.html',
                          {'lekar': email_adresa, 'uloga': uloga, 'odobreno': odobreno, 'vreme': vreme})
        else:
            return redirect('index')


def OdobriOdmor(request):
    """ kod koji radi UwU
    mail_subject = 'Aktivirajte vaš Pacijent akount'
    message = "hrf"
    to_email = "likneki55@gmail.com"
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    """

    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if True:  # try:
        if request.method == 'POST':
            id = request.POST['koga']
            kako = request.POST['kako']
            koga = request.POST['mail']

            if Odmor.objects.filter(id=id).exists():
                if kako == 'True':
                    od = Odmor.objects.filter(id=id)[0]
                    od.aktiviran = 1
                    od.save()
                    send_mail(
                        request.session['email'] + ' je odobrio vas zahtev za godisnji odmor',
                        "Vas zahtev za odlazak na godisnji odmor je odobren",
                        'aplikacijaklinika@gmail.com',
                        [koga],
                        fail_silently=False,
                    )
                else:
                    razlog = request.POST['razlog'].strip()
                    if razlog == "":
                        razlog = "Vas zahtev za odlazak na godisnji odmor je odbijen";
                    Odmor.objects.filter(id=id).delete()
                    send_mail(
                        request.session['email'] + ' je odbijo vas zahteva za godisnji odmor',
                        razlog,
                        'aplikacijaklinika@gmail.com',
                        [koga],
                        fail_silently=False,
                    )

                return redirect('OdobriOdmor')
        else:
            email = ''
            if 'email' in request.session:
                email = request.session['email']
            uloga = ''
            if 'uloga' in request.session:
                uloga = request.session['uloga']

            if uloga == 'ADMIN':
                org = Admin.objects.filter(email_adresa=email)[0].naziv_klinike
                niz = []
                for k in Odmor.objects.filter(aktiviran=0, klinika=org):
                    niz.extend([k])
                lekari = []
                for o in niz:
                    for l in Lekar.objects.all():
                        if o.lekar == l.email_adresa:
                            lekari.extend([{'prezime': l.prezime, 'o': o}])
                return render(request, 'odobriOdmor.html', {'niz': lekari})
            return HttpResponse('<h1>Error 400</h1>Bad request<br />Nemate pravo da pristupite ovoj stranici',
                                status=400)
    # except:
    #    return HttpResponse('<h1>Error 400</h1>Bad request<br />Pogresno ste uneli podatke', status=400)


def DaLiImamPregled(email):
    pregledi = Pregled.objects.filter(lekar=email)
    if pregledi.__len__() == 0:
        return None
    for preg in pregledi:
        duzina = 15
        try:
            duzina = TipPregleda.objects.filter(id=preg.tip_pregleda)[0].trajanje
        except:
            duzina = 15
            print("tip pregleda " + preg.tip_pregleda + " ne postoji")

        if datetime.datetime.now() >= preg.vreme and datetime.datetime.now() <= (preg.vreme + datetime.timedelta(
                minutes=duzina)):  # if datetime.datetime.now() <= preg.vreme and preg.vreme <= (datetime.datetime.now() + datetime.timedelta(minutes=duzina)):
            if preg.zakazan != "Prazno" and preg.id not in pregledani and preg.sala != -1:
                print("--------------------")
                print(preg.id)
                print('duzina ' + str(duzina))
                print(str(datetime.datetime.now()) + "<" + str(preg.vreme))
                print(datetime.datetime.now() <= preg.vreme)
                print(str(preg.vreme) + "<=" + str(datetime.datetime.now() + datetime.timedelta(minutes=duzina)))
                print(preg.vreme <= datetime.datetime.now() + datetime.timedelta(minutes=duzina))
                print("--------------------")
                return preg
    return None


def NapraviPregled(email):
    if DaLiImamPregled(email) is not None:
        return "<div class=\"square\"><label style=\"color:white\"><b>IMATE AKTIVAN PREGLED</b></label><form method=\"GET\" action=\"Pregledaj\" >"
    return " "


def NapraviRadniKalendar(email):
    odgovor = " "

    if DaLiImamPregled(email) is not None:
        odgovor += "<input type=\"submit\" class=\"meni\" value=\"ZAPOCNI\" ></form>" + "</div>"

    odgovor += "<h2>Radni Kalendar</h2> <table border=\"1\" class=\"table\" id=\"tabb1\"><tr><td></td>"

    odmora = -1
    odmorb = -1

    try:
        odmor = Odmor.objects.filter(lekar=email, aktiviran=1)[0]
        if datetime.datetime.now().month == odmor.vreme.month and datetime.datetime.now().year == odmor.vreme.year:
            odmora = odmor.vreme.day
            odmorb = odmora + odmor.duzina
    except:
        pass

    pregledi = Pregled.objects.filter(lekar=email, prihvacen="da")

    for i in range(1, monthrange(date.today().year, date.today().month)[1] + 1):
        tekst = "Nemata Zakazanih Pregleda"

        if i == 10 or i == 20 or i == 30:
            odgovor += "</tr><tr>"

        if odmora <= i <= odmorb:
            tekst = "Godisnji odmor"
            odgovor += "<td style=\"background-color:cyan; color:black;\"><div class=\"tooltip\">" + i.__str__() + "<span class=\"tooltiptext\">" + tekst + "</span></div></td>"
            pass

        iterator = 0
        for pregled in pregledi:
            if pregled.vreme.day == i and pregled.vreme.month == date.today().month and pregled.vreme.year == date.today().year:
                iterator += 1
                tekst = "Imate " + iterator.__str__() + " Zakazanih Pregleda"

        if tekst == "Nemata Zakazanih Pregleda":
            odgovor += "<td style=\"background-color:green; color:white;\"><div class=\"tooltip\">" + i.__str__() + "<span class=\"tooltiptext\">" + tekst + "</span></div></td>"
        elif tekst != "Godisnji odmor":
            odgovor += "<td style=\"background-color:red; color:black;\"><div class=\"tooltip\">" + i.__str__() + "<span class=\"tooltiptext\">" + tekst + "</span></div></td>"

    return odgovor + "</tr></table>" + \
           "<style>.tooltip {position: relative;display: inline-block;border-bottom: 1px dotted black;}.tooltip " \
           ".tooltiptext {visibility: hidden;width: 120px;background-color: black;color: #fff;text-align: " \
           "center;border-radius: 6px;padding: 5px 0;position: absolute;z-index: 1;}.tooltip:hover .tooltiptext {  " \
           "visibility: visible;} .table { font-family: arial, sans-serif; border-collapse: collapse; } " \
           ".td { border: 1px solid #dddddd; text-align: left; padding: 8px; } .th { border: 1px solid #dddddd; " \
           "text-align: left; padding: 8px; } .even { background-color: #4CAa50; } .tr{ " \
           "padding:5px; background-color: #60b060; } .th{ padding:5px; } input[type=submit]:hover { " \
           "background-color: #111; } input[type=submit]:hover:not(.meni) { background-color: #01b601; }</style> "


def NadjiPacijente(email, request):
    odgovor = "<h2>Vasi Pacijenti koje ste ranije pregledali</h2> <table border=\"1\" class=\"table\" id=\"tabb2\">"
    pacijenti = []
    pacijentiOBJ = []
    pp = Pregled.objects.filter(lekar=email)
    for p in pp:
        if p.zakazan != 'Prazno':
            pacijenti.extend([p.zakazan])

    for ppp in pacijenti:
        print(ppp)

    for pacijent in Pacijent.objects.all():
        if pacijent.email_adresa in pacijenti:
            pacijentiOBJ.extend([pacijent])

    if pacijentiOBJ.__len__() != 0:
        odgovor += "<tr class=\"tr\"><th class=\"th\">Ime</th><th class=\"th\">Prezime</th><th class=\"th\">Adresa " \
                   "Prebivališta</th><th class=\"th\">Država</th><th class=\"th\">Grad</th><th class=\"th\">Broja " \
                   "Telefona</th><th class=\"th\">Jedinstveni Broj Osiguranika</th><th></th></tr> "

        for pacijent in pacijentiOBJ:
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//////////////////////////////')
            odgovor += "<tr><td class=\"td\">" + pacijent.ime + "</td><td class=\"td\">" + pacijent.prezime + "</td>" \
                                                                                                              "<td class=\"td\">" + pacijent.adresa_prebivalista + "</td><td class=\"td\">" + pacijent.drzava + \
                       "</td><td class=\"td\">" + pacijent.grad + "</td><td class=\"td\">" + pacijent.broja_telefona + \
                       "</td><td class=\"td\">" + pacijent.jedinstveni_broj_osiguranika + "</td><td class=\"td\"><form method=\"POST\" action=\"ZdravstveniKarton\"> " + \
                       '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf.get_token(
                request) + "\">" + '<input type="hidden" name="kogap" value="' + pacijent.email_adresa + '">' + "<input type=\"submit\" value=\"Pogledaj Karton\"></form></td></tr>"
        return odgovor + "</table>"

    return "<h2>Nemate Pacijenata</h2>"


def ZdravstveniKarton(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    print("////////////////////////////////////////////////")
    print(request.POST['kogap'])
    pacijent = Pacijent.objects.filter(email_adresa=request.POST['kogap'])[0]
    return render(request, "zdravstveniKarton.html",
                  {'pacijent': pacijent})


def PogledajStanje(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    email = ""
    if 'email' in request.session:
        email = request.session['email']
    mapa = VratiFinansije(email)
    dan = PregledaDan(email)
    mesec = PregledaMesec(email)
    godina = PregledaGodina(email)
    avgKlinije = AvgKlinike(email)
    avgLekar = AvgLekara(email)
    datumNum = datumi(email)
    return render(request, "pogledajStanje.html",
                  {'map': mapa, 'dan': dan, 'mesec': mesec, 'godina': godina, 'avg': avgKlinije, 'lekar': avgLekar,
                   'datum': datumNum})


def PregledaDan(email):
    rez = []
    klinika = Admin.objects.filter(email_adresa=email)[0].naziv_klinike

    bdate = datetime.datetime.now()
    bdate = bdate.replace(hour=23, minute=59, second=59)
    sdate = bdate.replace(hour=0, minute=0, second=1)

    for i in range(1, 7):
        tren = 0

        for preg in Pregled.objects.filter(klinika=klinika, vreme__range=[sdate, bdate]):
            if preg.zakazan != "Prazno":
                tren += 1

        rez.append(tren)
        bdate = bdate - datetime.timedelta(days=1)
        sdate = bdate.replace(hour=0, minute=0, second=1)

    return rez[::-1]


def PregledaMesec(email):
    rez = []
    klinika = Admin.objects.filter(email_adresa=email)[0].naziv_klinike

    bdate = datetime.datetime.now()
    bdate = bdate.replace(hour=23, minute=59, second=59)
    sdate = bdate.replace(hour=0, minute=0, second=1) - datetime.timedelta(days=7)

    for i in range(1, 7):
        tren = 0

        for preg in Pregled.objects.filter(klinika=klinika, vreme__range=[sdate, bdate]):
            if preg.zakazan != "Prazno":
                tren += 1

        rez.append(tren)
        bdate = bdate - datetime.timedelta(days=7)
        sdate = bdate.replace(hour=0, minute=0, second=1) - datetime.timedelta(days=7)

    return rez[::-1]


def PregledaGodina(email):
    rez = []
    klinika = Admin.objects.filter(email_adresa=email)[0].naziv_klinike

    bdate = datetime.datetime.now()
    bdate = bdate.replace(hour=23, minute=59, second=59, day=29)
    sdate = bdate.replace(hour=0, minute=0, second=1, day=1)

    for i in range(1, 7):
        tren = 0

        for preg in Pregled.objects.filter(klinika=klinika, vreme__range=[sdate, bdate]):
            if preg.zakazan != "Prazno":
                tren += 1

        rez.append(tren)
        bdate = bdate - datetime.timedelta(days=29)
        sdate = bdate.replace(hour=0, minute=0, second=1, day=1)

    return rez[::-1]


def AvgKlinike(email):
    rez = 0
    klinika = Admin.objects.filter(email_adresa=email)[0].naziv_klinike

    tren = 0

    for preg in Pregled.objects.filter(klinika=klinika):
        if preg.zakazan != "Prazno":
            tren += 1
            rez += preg.ocenaKlinike

    return rez / tren


def AvgLekara(email):
    rez = "<table border=10><tr><th>Ime Lekara</th><th>Prezime Lekara</th><th>Email Adresa Lekara</th><th>Prosecna Ocena Lekara</th></tr>"
    klinika = Admin.objects.filter(email_adresa=email)[0].naziv_klinike

    for lekar in Lekar.objects.filter(radno_mesto=klinika):
        tren = 0
        pp = 0
        for preg in Pregled.objects.filter(klinika=klinika, lekar=lekar):
            if preg.zakazan != "Prazno":
                tren += 1
                pp += preg.ocenaKlinike
        if tren == 0:
            tren = 1
        if "[NPL]" in lekar.ime:
            rez += "<tr><td align='center'>" + lekar.ime[
                                               5:] + "</td><td align='center'>" + lekar.prezime + "</td><td align='center'>" + lekar.email_adresa + "</td><td align='center'>" + str(
                pp / tren) + "</td></tr>"
        else:
            rez += "<tr><td align='center'>" + lekar.ime + "</td><td align='center'>" + lekar.prezime + "</td><td align='center'>" + lekar.email_adresa + "</td><td align='center'>" + str(
                pp / tren) + "</td></tr>"

    return rez + "</table>"


def datumi(email):
    """
    var items = [
      [1, 2],
      [3, 4],
      [5, 6]
    ];
    """
    rez = "var datumi = ["
    klinika = Admin.objects.filter(email_adresa=email)[0].naziv_klinike

    for preg in Pregled.objects.filter(klinika=klinika):
        if preg.zakazan != "Prazno":
            cena = str(TipPregleda.objects.filter(id=preg.tip_pregleda)[0].cena)
            numvremena = time.mktime(preg.vreme.timetuple())
            rez += "[" + str(numvremena) + ", " + cena + "],"

    return rez[:-1] + "];"


def VratiFinansije(email):
    odgovor = "<h2>Finansije</h2><table border=\"1\" class=\"table\" id=\"tabb2\">"

    klinika = admin = Admin.objects.filter(email_adresa=email)[0].naziv_klinike
    ukupno = 0

    bdate = datetime.datetime.now()
    sdate = bdate.replace(year=2000)

    odgovor += "<tr>" \
               "<th>" + "Ko" + "</th>" \
                               "<th>" + "Kada" + "</th>" \
                                                 "<th>" + "Cena" + "</th>" \
                                                                   "</tr>"

    for preg in Pregled.objects.filter(klinika=klinika, vreme__range=[sdate, bdate]):
        if preg.zakazan != "Prazno":
            odgovor += "<tr>" + \
                       "<td>" + preg.zakazan.__str__() + "</td>" \
                                                         "<td>" + preg.vreme.__str__() + "</td>" \
                                                                                         "<td>" + (
                               len(preg.tip_pregleda) * 100 + len(preg.sala) * 10).__str__() + " din</td>" \
                                                                                               "</tr>"
            ukupno += len(preg.tip_pregleda) * 100 + len(preg.sala) * 10

    odgovor += "<tr>" \
               "<td></td>" \
               "<td style=\"text-align: right;\"><b>" + "Ukupno:" + "</b></td>" \
                                                                    "<td><b>" + ukupno.__str__() + " din</b></td>" \
                                                                                                   "</tr>"

    if ukupno == 0:
        return "<h2>Nemate jos ni jedan odradjen pregled</h2>"

    return odgovor + "</table>" + "</tr></table>" + \
           "<style>.tooltip {position: relative;display: inline-block;border-bottom: 1px dotted black;}.tooltip " \
           ".tooltiptext {visibility: hidden;width: 120px;background-color: black;color: #fff;text-align: " \
           "center;border-radius: 6px;padding: 5px 0;position: absolute;z-index: 1;}.tooltip:hover .tooltiptext {  " \
           "visibility: visible;} .table { font-family: arial, sans-serif; border-collapse: collapse; } " \
           ".td { border: 1px solid #dddddd; text-align: left; padding: 8px; } .th { border: 1px solid #dddddd; " \
           "text-align: left; padding: 8px; } .even { background-color: #4CAa50; } .tr{ " \
           "padding:5px; background-color: #60b060; } .th{ padding:5px; } input[type=submit]:hover { " \
           "background-color: #111; } input[type=submit]:hover:not(.meni) { background-color: #01b601; }</style> "


def OdobriAkaunt(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    try:
        if request.method == 'POST':
            id = request.POST['koga']
            kako = request.POST['kako']

            if Pacijent.objects.filter(email_adresa=id).exists():
                if kako == 'True':
                    od = Pacijent.objects.filter(email_adresa=id)[0]

                    od.aktiviran = 0
                    od.save()
                    try:
                        current_site = get_current_site(request)
                        mail_subject = 'Aktivirajte vaš Pacijent akount'
                        message = render_to_string('acc_active_email.html', {
                            'user': od,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(od.pk)),
                            'token': account_activation_token.make_token(od),
                        })
                        to_email = id
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                    except:
                        pass

                else:
                    Pacijent.objects.filter(email_adresa=id).delete()
                    try:
                        mail_subject = 'Odbijena je vaša registracija'

                        to_email = id
                        email = EmailMessage(
                            mail_subject, "Vaša registracija je odbijena!", to=[to_email]
                        )
                        email.send()
                    except:
                        pass

                return redirect('OdobriAkaunt')
        else:
            email = ''
            if 'email' in request.session:
                email = request.session['email']
            uloga = ''
            if 'uloga' in request.session:
                uloga = request.session['uloga']

            if uloga == 'ADMIN':
                org = Admin.objects.filter(email_adresa=email)[0].naziv_klinike
                niz = []
                for k in Pacijent.objects.filter(aktiviran=-1):
                    niz.extend([k])
                return render(request, 'odobriAkaunt.html', {'niz': niz})
            return HttpResponse('<h1>Error 400</h1>Bad request<br />Nemate pravo da pristupite ovoj stranici',
                                status=400)
    except:
        return HttpResponse('<h1>Error 400</h1>Bad request<br />Pogresno ste uneli podatke', status=400)


# deo koji pripada Jovanu Corilicu sw48/2017
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Pacijent.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        user.aktiviran = 1
        user.save()
        # return redirect('home')
        request.session['uloga'] = "NEULOGOVAN"
        return HttpResponse("Vaš akount je napravljen i sada možete da ga koristite!")
    else:
        return HttpResponse('Aktivacioni link nije validan')


# -----------------------------------------------
def OdobriPregled(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    # try:
    if request.method == 'POST':
        id = request.POST['koga']
        kako = request.POST['kako']

        if Pregled.objects.filter(id=id).exists():
            if kako == 'True':

                gde = request.POST['gde']
                kada = request.POST['kada']

                od = Pregled.objects.filter(id=id)[0]
                od.prihvacen = "da"
                od.sala = gde
                od.vreme = kada
                od.save()
                try:
                    mail_subject = 'Vaš zahtev za pregled je prihvaćen'

                    email2 = Pregled.objects.get(id=id)
                    to_email = email2.zakazan
                    try:
                        email = EmailMessage(
                            mail_subject,
                            "Vaš zahtev za pregled je prihvaćen i doktor će vas čekati u vremenu koji ste napisali!",
                            to=[to_email]
                        )
                        email.send()
                    except:
                        print("Pogresan email format. molimo vas da unesete pravi email")
                except:
                    pass
            elif kako == 'Ok':
                uloga = ""
                if 'uloga' in request.session:
                    uloga = request.session['uloga']
                kk = Pregled.objects.all()
                sale = Sala.objects.all()
                mapa = napraviMapuTerminaSala(kk, sale)
                preg = od = Pregled.objects.filter(id=id)[0]
                trajanje = TipPregleda.objects.filter(id=preg.tip_pregleda)[0].trajanje
                cell = prviSlobodan(preg, sale, trajanje)
                for i in range(len(sale)):
                    print(sale[i].naziv + " " + str(cell[i]))
                    sale[i].index = cell[i]
                return render(request, 'odaberiSalu.html', {'pregled': preg, 'mapa': mapa, 'sale': sale,
                                                            'trajanje': trajanje})  # , 'vremeNiz':cell})
            else:
                Pregled.objects.filter(id=id).delete()
                try:
                    mail_subject = 'Odbijen je vaš zahtev za pregled'
                    email2 = Pregled.objects.get(id=id)
                    to_email = email2.zakazan
                    email = EmailMessage(
                        mail_subject, "Odbijen je vaš zahtev za pregled!", to=[to_email]
                    )
                    email.send()
                except:
                    pass

            return redirect('OdobriPregled')
    else:
        email = ''
        if 'email' in request.session:
            email = request.session['email']
        uloga = ''
        if 'uloga' in request.session:
            uloga = request.session['uloga']

        if uloga == 'ADMIN':
            niz = []
            kl = Admin.objects.filter(email_adresa=request.session['email'])[0].naziv_klinike
            for k in Pregled.objects.filter(prihvacen="ne", klinika=kl):
                niz.extend([k])

            pregledi = []
            for o in niz:
                for l in Pacijent.objects.all():
                    if o.zakazan == l.email_adresa:
                        pregledi.extend([{'pacijent': l, 'pregled': o}])
            return render(request, 'odobriPregled.html', {'niz': pregledi})
        return HttpResponse('<h1>Error 400</h1>Bad request<br />Nemate pravo da pristupite ovoj stranici',
                            status=400)


def prviSlobodan(pregled, sale, trajanje):
    odgovor = []
    vreme = pregled.vreme

    for sala in sale:
        slvreme = vreme
        while not proveriTermin2(slvreme, sala, trajanje):
            slvreme += datetime.timedelta(minutes=15)
        odgovor.append(slvreme)
    return odgovor


def Pregledaj(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        ko = request.POST['ko']
        koga = request.POST['koga']
        kako = request.POST['kako']

        lek = Lekar.objects.filter(email_adresa=ko)[0]

        preg = Pregled.objects.filter(id=kako)[0]
        preg.prihvacen = "ne"
        preg.save()

        pac = Pacijent.objects.filter(email_adresa=koga)[0]
        if request.POST['sifra_bolesti'] not in pac.sifra_bolesti:
            pac.sifra_bolesti += "<br>" + request.POST['sifra_bolesti']
        pac.diagnoza += "<br>" + datetime.datetime.now().__str__().split('.')[0] + " :<br><br>" + request.POST[
            'diagnoza']
        if request.POST['lekovi'] not in pac.lekovi:
            pac.lekovi += "<br>" + request.POST['lekovi']
        pac.dioptrija = request.POST['dioptrija']
        if request.POST['alergije_na_lek'] not in pac.alergije_na_lek:
            pac.alergije_na_lek += "<br>" + request.POST['alergije_na_lek']
        if request.POST['visina'] != "Nema" and request.POST['visina'] != '':
            pac.visina = request.POST['visina']
        if request.POST['tezina'] != "Nema" and request.POST['tezina'] != '':
            pac.tezina = request.POST['tezina']
        try:
            if pac.krvna_grupa == "Nema":
                pac.krvna_grupa = request.POST['krvna_grupa']
        except:
            print("krvna grupa vec postavljena")
        pac.save()

        pregledani.append(kako)
        return render(request, 'zakaziOpet.html',
                      {'ko': ko, 'koga': koga, 'kako': kako, 'klinika': lek.radno_mesto, 'lekar': lek.email_adresa,
                       'sala': preg.sala, 'tip_pregleda': preg.tip_pregleda,
                       'vreme': (preg.vreme + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')})
    else:
        email = ''
        if 'email' in request.session:
            email = request.session['email']
        uloga = ''
        if 'uloga' in request.session:
            uloga = request.session['uloga']

        if uloga == 'LEKAR':
            pregled = DaLiImamPregled(email)
            pacijent = None
            for pac in Pacijent.objects.all():
                if pregled.zakazan == pac.email_adresa:
                    pacijent = pac

            if pacijent is None or pregled is None:
                return HttpResponse('<h1>Error 400</h1>Bad request<br />Doslo je do greske', status=400)
            return render(request, 'pregledaj.html', {'pregled': pregled, 'pacijent': pacijent, 'email': email})
        return HttpResponse('<h1>Error 400</h1>Bad request<br />Nemate pravo da pristupite ovoj stranici',
                            status=400)


def ZakaziOpet(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    vr = datetime.datetime.strptime(request.POST['vreme'], '%Y-%m-%d %H:%M:%S')
    i = Pregled.objects.count()
    while Pregled.objects.count() == i:
        manualTerminLekar(klinika=request.POST['klinika'], lekar=request.POST['lekar'], sala=request.POST['sala'],
                          tip_pregleda=request.POST['tip_pregleda'], vreme=vr.strftime('%Y-%m-%d %H:%M:%S'),
                          zakazan=request.POST['koga'])
        vr = vr + datetime.timedelta(hours=1)
    ###########################################
    kome = []
    for ada in Admin.objects.filter(naziv_klinike=request.POST['klinika']):
        kome.append(ada.email_adresa)
    for ww in kome:
        try:
            send_mail(
                request.session['email'] + ' zeli da zakaze pregled sa pcaijentom ' + request.POST['koga'],
                request.session['email'] + ' zeli da zakaze pregled sa pcaijentom ' + request.POST[
                    'koga'] + ". Molimo vas da pogledate sajt klinike za vise informacija, i da odlucite da li odobravate ovaj pregled",
                'aplikacijaklinika@gmail.com',
                [ww],
                fail_silently=False,
            )
        except:
            print('invalid email')
    return redirect('index')


def DodajTip(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        id = request.POST['id']
        ime = request.POST['ime']
        trajanje = request.POST['trajanje']
        cena = request.POST['cena']

        if TipPregleda.objects.filter(id=id).exists() or TipPregleda.objects.filter(ime=ime).exists():
            messages.info(request, "_")
            return redirect('DodajTip')
        while True:
            try:
                tip = TipPregleda.objects.create(id=id, ime=ime, trajanje=trajanje, cena=cena)
                tip.save()
                storage = messages.get_messages(request)
                storage.used = True
                return redirect('index')
            except:
                pass
    else:
        return render(request, 'dodajTip.html')


def PogledajTipove(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    kk = TipPregleda.objects.all()
    return render(request, 'pogledajTipove.html', {'tipovi': kk})


def PogledajTip(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    odabrani = None
    for tip in TipPregleda.objects.all():
        try:
            if request.POST[tip.id] is not None:
                odabrani = tip
        except:
            pass
    if odabrani is not None:
        return render(request, 'pogledajTip.html', {'tip': odabrani})


def IzmeniTip(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    if request.method == 'POST':
        ime = request.POST['ime']
        cena = request.POST['cena']
        duzina = request.POST['trajanje']

        if TipPregleda.objects.filter(id=request.POST['koga']).exists():
            k = TipPregleda.objects.filter(id=request.POST['koga'])[0]
            if not TipPregleda.objects.filter(ime=ime).exists():
                k.ime = ime
            k.cena = cena
            k.trajanje = duzina
            nijeZakazano = True

            for pregled in Pregled.objects.filter(tip_pregleda=request.POST['koga']):
                if pregled.vreme >= datetime.datetime.now():
                    nijeZakazano = False

            if nijeZakazano:
                k.save()
                return redirect('index')
            else:
                return HttpResponse('<h1>Error 400</h1>Bad request<br />Postoje zakazani termini ovog tipa pregleda',
                                    status=400)
        return redirect('index')
    else:
        return redirect('index')


def ObrisiTip(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    try:
        nijeZakazano = True

        for pregled in Pregled.objects.filter(tip_pregleda=request.POST['koga']):
            if pregled.vreme >= datetime.datetime.now():
                nijeZakazano = False

        if nijeZakazano:
            TipPregleda.objects.filter(id=request.POST['koga']).delete()
            return redirect('index')
        return HttpResponse('<h1>Error 400</h1>Bad request<br />Postoje zakazani termini ovog tipa pregleda',
                            status=400)
    except:
        return redirect('index')
