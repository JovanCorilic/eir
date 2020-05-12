from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from clinic.models import Pacijent, Admin, Klinika, Pregled
from django.contrib import messages
from datetime import date
from clinic.models import Lekar
from clinic.models import Sala
import datetime
import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


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
        try:
            if request.POST[pacijent.email_adresa] is not None:
                odabrani = pacijent
                return render(request, 'pogledajPacijenta.html', {'pacijent': odabrani})
        except:
            pass




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
            if request.POST[kli.email_adresa] is not None:
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
    try:
        Lekar.objects.filter(email_adresa=request.POST['koga']).delete()
        return redirect('index')
    except:
        return redirect('index')

def PogledajTermine(request):
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
    sala = Sala.objects.filter(id_klinike_kojoj_pripada=klinika, naziv=odabrani.sala)[0]

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

    return render(request, 'pogledajTermin.html', {'mapa': mapa, 'lekari': lekari, 'sale': sale, 'lekar':lekarid, 'sala':salaid, 'termin': Pregled.objects.filter(id=odabrani.id)[0]})


def ObrisiTermin(request):
    try:
        Pregled.objects.filter(id=request.POST['koga']).delete()
        return redirect('index')
    except:
        return redirect('index')

def IzmeniTermin(request):
    try:
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
    except:
        return HttpResponse('<h1>Error 400</h1>Bad request<br />Pogresno ste uneli podatke', status=400)


def DodajTermin(request):
    try:
        if request.method == 'POST':
            id = request.POST['broj']
            lekar = request.POST['lekar']
            sala = request.POST['sala']
            vreme = request.POST['vreme']
            tip_pregleda = request.POST['tip_pregleda']
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
                                    klinika = korinisk.klinika
                            for korinisk in Admin.objects.all():
                                if korinisk.email_adresa == email:
                                    klinika = korinisk.naziv_klinike
                            ter = Pregled.objects.create(id=id, klinika=klinika, zakazan="Prazno", lekar=lekar, sala=sala, tip_pregleda=tip_pregleda, vreme=vreme, sifra_bolesti="Prazno", diagnoza="Prazno", lekovi="Prazno")
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
            kk = Pregled.objects.filter(
                vreme__range=[date.today(), date.today() + datetime.timedelta(days=1)])
            mapa = napraviMapu2(kk, sale)

            lekari = Lekar.objects.filter(radno_mesto=klinika)
            sale = Sala.objects.filter(id_klinike_kojoj_pripada=klinika)
            return render(request, "dodajTermin.html", {'klinika': klinika ,'mapa': mapa, 'lekari': lekari, 'sale': sale, 'vreme': date.today()})
    except:
        return HttpResponse('<h1>Error 400</h1>Bad request', status=400)


def proveriTermin(vreme, sala, lekar, idd=-9999):
    try:
        for termin in Pregled.objects.all():
            if termin.sala == sala and termin.id != idd:
                if not (termin.vreme > vreme + datetime.timedelta(minutes=30) or termin.vreme + datetime.timedelta(minutes=30) < vreme):
                    return False
        for termin in Pregled.objects.all():
            if termin.lekar == lekar and termin.id != idd:
                if not (termin.vreme > vreme + datetime.timedelta(minutes=30) or termin.vreme + datetime.timedelta(
                        minutes=30) < vreme):
                    return False
        return True
    except:
        vreme = datetime.datetime.strptime(vreme, "%Y-%m-%d %H:%M:%S")
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
                    rezultat += "<div style=\"background-color:red;padding: 5px;display: inline\">" + (pregled.vreme + datetime.timedelta(minutes=30)).time().__str__() + "</div>" + "<div style=\"background-color:green;padding: 5px;display: inline\">" + (pregled.vreme + datetime.timedelta(minutes=30)).time().__str__() + "</div>"
                    trenutni = (pregled.vreme + datetime.timedelta(minutes=30)).time()
                    kraj=""
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
                        kraj=""
        rezultat += kraj + " - 24:00:00"
        rez += "\"" + rezultat + "\","
    return rez[:-1] + "]"


def autoTermin(request):
    for klinika in Klinika.objects.all():
        kk = Pregled.objects.filter(vreme__range=[date.today(), date.today() + datetime.timedelta(days=1)], klinika=klinika.naziv)
        if len(kk) == 0:
            for i in (6, 8, 10, 12, 14, 16, 18, 20):
                try:
                    print('iteracija ' + "za kliniku " + klinika.naziv)
                    sala = random.choice(Sala.objects.filter(id_klinike_kojoj_pripada=klinika.naziv))
                    lekar = random.choice(Lekar.objects.filter(radno_mesto=klinika.naziv))
                    vreme = datetime.datetime.today().replace(hour=i, minute=0, second=0)
                    manualTermin(lekar, sala, vreme, klinika.naziv, "Opsti Pregled", request)
                except:
                    print("nesto fali")
                    pass


def manualTermin(lekar, sala, vreme, klinika, tip_pregleda, request):
    print("usao")
    id = 1
    if Pregled.objects.filter(id=id).exists():
        while Pregled.objects.filter(id=id).exists():
            id += 1
    print("dodeljen id " + id.__str__())
    if not Pregled.objects.filter(id=id).exists():
        if proveriTermin(vreme, sala, lekar):
            ii = 0
            while True:
                ii += 1
                if ii >= 100:
                    return
                try:
                    ter = Pregled.objects.create(id=id, klinika=klinika, zakazan="Prazno", lekar=lekar, sala=sala,
                                                 tip_pregleda=tip_pregleda, vreme=vreme, sifra_bolesti="Prazno", diagnoza="Prazno",
                                                 lekovi="Prazno")
                    ter.save()
                    print("sacuvao :)")
                    return
                except:
                    pass

#-----------------------------------------------------------------------------------------------------------------------
#nemoj ispod ove linije raditi

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Pacijent.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.aktiviran = 1
        user.save()
        # return redirect('home')
        return HttpResponse('Hvala na vašoj email konfrmacije, sada možete da se ulogujete.')
    else:
        return HttpResponse('Aktivacioni link nije validan')

def registracijaPacijent(request):
    try:
        if request.method == 'POST':
            """email_adresa = request.POST.get('email', "")
            lozinka = request.POST.get('sifra', "")
            ime = request.POST.get('ime', "")
            prezime = request.POST.get('prezime', "")
            adresa_prebivalista = request.POST.get('adresa', "")
            grad = request.POST.get('grad', "")
            drzava = request.POST.get('drzava', "")
            broja_telefona = request.POST.get('broj', "")
            jedinstveni_broj_osiguranika = request.POST.get('jedinstveni', "")"""

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
                                               visina="Prazno", tezina="Prazno", krvna_grupa="Prazno", aktiviran=0)

            pacijent.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktivirajte vaš Pacijent akount'
            message = render_to_string('acc_active_email.html', {
                'user': pacijent,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(pacijent.pk)),
                'token': account_activation_token.make_token(pacijent),
            })
            to_email = email_adresa
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Molim vas potvrdite vašu email registraciju.')

            # print("napravljen pacijent " + ime)
            # return redirect('loginKorisnik')
        else:
            return render(request, 'pacijent/registracijaPacijent.html')
    except:
        return redirect('registracijaPacijent')

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

def pretragaKlinikaPacijent(request):
    if request.method == 'POST':
        if 'pretragaNaziv' in request.POST:
            pretrazuje = "naziv"
        else:
            pretrazuje = "opis"
        sadrzaj = request.POST['unosPretraga']
        #klinike = Klinika.objects.all()
        if(pretrazuje == "naziv"):
            klinike = Klinika.objects.filter(naziv__icontains = sadrzaj )
        else:
            klinike = Klinika.objects.filter(opis__icontains = sadrzaj)
        request.session['lokacija'] = 3
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'klinike': klinike})
    else:
        klinike = Klinika.objects.all()
        request.session['lokacija'] = 3
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'klinike': klinike})

def prikazLekaraKlinikePacijent(request):
    if request.method == 'POST':
        nazivKlinike = request.POST['nazivKlinike']
        naziv = nazivKlinike.split()
        request.session['nazivKlinike'] = naziv[3]
        lekari = Lekar.objects.filter(radno_mesto = naziv[3])
        request.session['lokacija'] = 3.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'lekari': lekari})
    else:
        request.session['lokacija'] = 3.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija']})

def sortiranjeLekaraPacijent(request):
    if request.method == 'POST':

        if 'sortirajIme' in request.POST:
            tip = 'ime'
        elif 'sortirajPrezime' in request.POST:
            tip = 'prezime'
        elif 'sortirajEmail' in request.POST:
            tip = 'email_adresa'
        else:
            tip = 'pozicija'

        lekari = Lekar.objects.filter(radno_mesto=request.session['nazivKlinike']).order_by(tip)

        request.session['lokacija'] = 3.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'lekari': lekari})
    else:
        request.session['lokacija'] = 3.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija']})

def pretragaLekaraPacijent(request):
    if request.method == 'POST':
        if 'pretragaIme' in request.POST:
            pretrazuje = "ime"
        else:
            pretrazuje = "prezime"
        sadrzaj = request.POST['unosPretraga']

        if (pretrazuje == "ime"):
            lekari = Lekar.objects.filter(radno_mesto=request.session['nazivKlinike'], ime__icontains=sadrzaj)
        else:
            lekari = Lekar.objects.filter(radno_mesto=request.session['nazivKlinike'], prezime__icontains=sadrzaj)
        request.session['lokacija'] = 3.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'lekari': lekari})
    else:
        request.session['lokacija'] = 3.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija']})

def prikaziBrzePreglede(request):
    autoTermin(request)
    if request.method == 'POST':

        nazivKlinike = request.POST['nazivKlinike']
        naziv = nazivKlinike.split()
        request.session['nazivKlinike'] = naziv[4]
        pregledi = Pregled.objects.filter(klinika=naziv[4], zakazan="Prazno", vreme__gte = datetime.datetime.now())
        lekari = Lekar.objects.filter(radno_mesto=naziv[4])
        request.session['lokacija'] = 3.6
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'pregledi': pregledi, 'lekari': lekari})
    else:
        request.session['lokacija'] = 3.6
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija']})

def zakaziBrzPregled(request):
    autoTermin(request)
    if request.method == 'POST':
        idPregled = request.POST['id123']

        pregled = Pregled.objects.get(id=idPregled)
        pregled.zakazan = request.session['email']
        pregled.save()

        pregledi = Pregled.objects.filter(klinika=request.session['nazivKlinike'], zakazan="Prazno", vreme__gte = datetime.datetime.now())
        lekari = Lekar.objects.filter(radno_mesto=request.session['nazivKlinike'])
        request.session['lokacija'] = 3.6
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'pregledi': pregledi, 'lekari': lekari})

    else:
        request.session['lokacija'] = 3.6
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija']})

def sviPreglediPacijent(request):
    if request.method == 'POST':
        pregledi = Pregled.objects.filter(zakazan=request.session['email']).order_by('-vreme')
        request.session['lokacija'] = 4
        lekari = Lekar.objects.all()
        sada = datetime.datetime.now()
        for i in range(len(pregledi)):
            temp = pregledi[i].vreme - datetime.timedelta(days=1)
            if pregledi[i].vreme > sada and sada < temp:
                pregledi[i].temp = "da"
            else:
                pregledi[i].temp = "ne"

        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'pregledi': pregledi, 'lekari': lekari })
    else:
        pregledi = Pregled.objects.filter(zakazan=request.session['email']).order_by('-vreme')
        request.session['lokacija'] = 4

        lekari = Lekar.objects.all()
        
        sada = datetime.datetime.now()
        for i in range(len(pregledi)):
            temp = pregledi[i].vreme - datetime.timedelta(days=1)
            if pregledi[i].vreme > sada and sada < temp:
                pregledi[i].temp = "da"
            else:
                pregledi[i].temp = "ne"

        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'pregledi': pregledi, 'lekari': lekari})

def otkaziPregledPacijent(request):
    if request.method == 'POST':
        broj = request.POST['id123']
        pregled = Pregled.objects.get(id = broj)
        pregled.zakazan = "Prazno"
        pregled.save()
        provera = datetime.datetime.now() - datetime.timedelta(days=1)
        pregledi = Pregled.objects.filter(zakazan=request.session['email']).order_by('vreme')
        request.session['lokacija'] = 4
        lekari = Lekar.objects.all()
        sada = datetime.datetime.now()
        for i in range(len(pregledi)):
            temp = pregledi[i].vreme - datetime.timedelta(days=1)
            if pregledi[i].vreme > sada and sada < temp:
                pregledi[i].temp = "da"
            else:
                pregledi[i].temp = "ne"

        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'pregledi': pregledi, 'lekari': lekari,
                       'sada': datetime.datetime.now(), 'provera': provera})
    else:
        pregledi = Pregled.objects.filter(zakazan=request.session['email']).order_by('-vreme')
        request.session['lokacija'] = 4

        lekari = Lekar.objects.all()

        sada = datetime.datetime.now()
        for i in range(len(pregledi)):
            temp = pregledi[i].vreme - datetime.timedelta(days=1)
            if pregledi[i].vreme > sada and sada < temp:
                pregledi[i].temp = "da"
            else:
                pregledi[i].temp = "ne"

        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'pregledi': pregledi, 'lekari': lekari})
