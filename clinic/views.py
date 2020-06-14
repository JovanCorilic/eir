from calendar import monthrange
from time import strptime

from clinic.models import Admin, Klinika, Odmor
from pacijent.models import Pacijent, Pregled
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
from django.core.mail import EmailMessage


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
        pacijenti = NadjiPacijente(email)
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
                return render(request, 'pogledajPacijenta.html', {'pacijent': odabrani})
        except:
            pass


def pogledajSale(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    uloga = ""
    if 'uloga' in request.session:
        uloga = request.session['uloga']

    sale = Sala.objects.all()
    return render(request, 'pogledajSale.html', {'sale': sale, 'uloga': uloga})


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
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
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

            k.save()
            return redirect('index')
        return redirect('index')
    else:
        return redirect('index')


def ObrisiLekara(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    try:
        Lekar.objects.filter(email_adresa=request.POST['koga']).delete()
        return redirect('index')
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
        idd = odabrani.sala.split('-')
        sala = Sala.objects.filter(id_klinike_kojoj_pripada=klinika, id=idd[0])[0]

    lekarid = 0
    salaid = 0
    ii = 0
    for le in lekari:
        if le.email_adresa == lekar.email_adresa:
            lekarid = ii
            break
        ii += 1

    ii = 0
    for le in sale:
        if le.naziv == sala.naziv:
            salaid = ii
            break
        ii += 1

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
                            ter = Pregled.objects.create(id=id, klinika=klinika, zakazan="Prazno", lekar=lekar,
                                                         sala=sala, tip_pregleda=tip_pregleda,
                                                         vreme=vreme.__str__().split(".")[0],
                                                         sifra_bolesti="Prazno", diagnoza="Prazno", lekovi="Prazno",
                                                         prihvacen='da')
                            ter.save()
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
                           'lekar': email, 'vreme': date.today()})
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

                    sala = random.choice(Sala.objects.filter(id_klinike_kojoj_pripada=klinika.naziv))
                    lekar = random.choice(Lekar.objects.filter(radno_mesto=klinika.naziv))
                    vreme = datetime.datetime.now().replace(hour=i, minute=0, second=0)

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

                    ter = Pregled.objects.create(id=id, klinika=klinika, zakazan="Prazno", lekar=lekar, sala=sala,
                                                 tip_pregleda=tip_pregleda, vreme=vreme.__str__().split(".")[0],
                                                 sifra_bolesti="Prazno",
                                                 diagnoza="Prazno", lekovi="Prazno", prihvacen="da")

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
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    try:
        if request.method == 'POST':
            id = request.POST['koga']
            kako = request.POST['kako']

            if Odmor.objects.filter(id=id).exists():
                if kako == 'True':
                    od = Odmor.objects.filter(id=id)[0]
                    od.aktiviran = 1
                    od.save()
                else:
                    Odmor.objects.filter(id=id).delete()

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
    except:
        return HttpResponse('<h1>Error 400</h1>Bad request<br />Pogresno ste uneli podatke', status=400)


def DaLiImamPregled(email):
    pregledi = Pregled.objects.filter(lekar=email)
    if pregledi.__len__() == 0:
        return None
    for preg in pregledi:
        if preg.vreme <= datetime.datetime.now() <= preg.vreme + datetime.timedelta(minutes=30):
            if preg.zakazan != "Prazno" and preg.id not in pregledani:
                print("--------------------")
                print(preg.id)
                print("se nalazi?")
                print(preg.id in pregledani)
                for sas in pregledani:
                    print(sas)
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
            if pregled.vreme.day == i:
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


def NadjiPacijente(email):
    odgovor = "<h2>Vasi Pacijenti</h2> <table border=\"1\" class=\"table\" id=\"tabb2\">"

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
                   "Telefona</th><th class=\"th\">Jedinstveni Broj Osiguranika</th></tr> "

        for pacijent in pacijentiOBJ:
            odgovor += "<tr><td class=\"td\">" + pacijent.ime + "</td><td class=\"td\">" + pacijent.prezime + "</td>" \
                                                                                                              "<td class=\"td\">" + pacijent.adresa_prebivalista + "</td><td class=\"td\">" + pacijent.drzava + \
                       "</td><td class=\"td\">" + pacijent.grad + "</td><td class=\"td\">" + pacijent.broja_telefona + \
                       "</td><td class=\"td\">" + pacijent.jedinstveni_broj_osiguranika + "</td> "
        return odgovor + "</table>"

    return "<h2>Nemate Pacijenata</h2>"


def PogledajStanje(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    email = ""
    if 'email' in request.session:
        email = request.session['email']
    map = VratiFinansije(email)
    return render(request, "pogledajStanje.html", {'map': map})


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

#deo koji pripada Jovanu Corilicu sw48/2017
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Pacijent.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None :
        user.aktiviran = 1
        user.save()
        # return redirect('home')
        request.session['uloga']="NEULOGOVAN"
        return HttpResponse("Vaš akount je napravljen i sada možete da ga koristite!")
    else:
        return HttpResponse('Aktivacioni link nije validan')
#-----------------------------------------------
def OdobriPregled(request):
    if 'uloga' not in request.session or request.session['uloga'] == 'NEULOGOVAN':
        return redirect('index')
    # try:
    if request.method == 'POST':
        id = request.POST['koga']
        kako = request.POST['kako']

        if Pregled.objects.filter(id=id).exists():
            if kako == 'True':
                od = Pregled.objects.filter(id=id)[0]
                od.prihvacen = "da"
                od.save()
                try:
                    mail_subject = 'Vaš zahtev za pregled je prihvaćen'

                    email2 = Pregled.objects.get(id=id)
                    to_email = email2.zakazan
                    email = EmailMessage(
                        mail_subject, "Vaš zahtev za pregled je prihvaćen i doktor će vas čekati u vremenu koji ste napisali!", to=[to_email]
                    )
                    email.send()
                except:
                    pass
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
            for k in Pregled.objects.filter(prihvacen="ne"):
                niz.extend([k])

            pregledi = []
            for o in niz:
                for l in Pacijent.objects.all():
                    if o.zakazan == l.email_adresa:
                        pregledi.extend([{'pacijent': l, 'pregled': o}])
            return render(request, 'odobriPregled.html', {'niz': pregledi})
        return HttpResponse('<h1>Error 400</h1>Bad request<br />Nemate pravo da pristupite ovoj stranici',
                            status=400)


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
        pac.sifra_bolesti = request.POST['sifra_bolesti']
        pac.diagnoza += "\n" + datetime.datetime.now().__str__() + " :\n\t" + request.POST['diagnoza']
        pac.lekovi = request.POST['lekovi']
        pac.dioptrija = request.POST['dioptrija']
        pac.alergije_na_lek = request.POST['alergije_na_lek']
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
        manualTermin(klinika=request.POST['klinika'], lekar=request.POST['lekar'], sala=request.POST['sala'],
                     tip_pregleda=request.POST['tip_pregleda'], vreme=vr.strftime('%Y-%m-%d %H:%M:%S'), request=request)
        vr = vr + datetime.timedelta(hours=1)
    return redirect('index')
