from clinic.models import  Admin, Klinika, Odmor
from pacijent.models import Pacijent, Pregled, Operacije
from django.contrib import messages
from datetime import date
from clinic.models import Lekar
from clinic.models import Sala
import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from clinic.views import autoTermin
# Create your views here.


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Pacijent.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.aktiviran = 0
        user.save()
        # return redirect('home')
        return HttpResponse('Hvala na vašoj email konfrmacije, sada čekate potvrdu administratora.')
    else:
        return HttpResponse('Aktivacioni link nije validan')


def registracijaPacijent(request):
    try:
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
                return render(request, 'registracijaPacijent.html', {'poruka':"Email adresa je vec zauzeta!"})

            elif "[" in ime or "]" in ime or "[NPL]" in ime:
                # print("ime ne sme da sadrzi [NPL]")
                return render(request, 'registracijaPacijent.html', {'poruka':"Ime ne sme da sadrzi karaktere [ ili ] !"})

            pacijent = Pacijent.objects.create(email_adresa=email_adresa, lozinka=lozinka, ime=ime, prezime=prezime,
                                               broja_telefona=broja_telefona,
                                               jedinstveni_broj_osiguranika=jedinstveni_broj_osiguranika,
                                               adresa_prebivalista=adresa_prebivalista, grad=grad, drzava=drzava,
                                               sifra_bolesti="Prazno", datum=date.today().strftime("%d/%m/%Y"),
                                               diagnoza="Prazno", lekovi="Prazno",
                                               dioptrija="Prazno", alergije_na_lek="Prazno",
                                               visina="Prazno", tezina="Prazno", krvna_grupa="Prazno", aktiviran=-1)

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
        else:
            return render(request, 'pacijent/registracijaPacijent.html')
    except:
        print("Ovde je prosao!\n")
        return redirect('registracijaPacijent')


# return render(request, 'pogledajLekare.html', {'lekari': kk})

def glavnaStranicaPacijent(request):
    if request.method == 'POST':
        request.session['lokacija'] = 0
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'email': request.session['email'], 'ime': request.session['ime'],
                       'prezime': request.session['prezime'],
                       'lokacija': request.session['lokacija']})
    else:
        request.session['lokacija'] = 0
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'email': request.session['email'], 'ime': request.session['ime'],
                       'prezime': request.session['prezime'],
                       'lokacija': request.session['lokacija']})


def licniPodaciPacijent(request):
    if request.method == 'POST':
        request.session['lokacija'] = 1

        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'email': request.session['email'], 'ime': request.session['ime'],
                       'prezime': request.session['prezime'], 'lokacija': request.session['lokacija'],
                       'lozinka': request.session['lozinka'], 'adresa': request.session['adresa_prebivalista'],
                       'grad': request.session['grad'], 'drzava': request.session['drzava'],
                       'broj': request.session['broja_telefona'],
                       'jedinstven': request.session['jedinstveni_broj_osiguranika']})

    else:
        request.session['lokacija'] = 1
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'email': request.session['email'], 'ime': request.session['ime'],
                       'prezime': request.session['prezime'], 'lokacija': request.session['lokacija'],
                       'lozinka': request.session['lozinka'], 'adresa': request.session['adresa_prebivalista'],
                       'grad': request.session['grad'], 'drzava': request.session['drzava'],
                       'broj': request.session['broja_telefona'],
                       'jedinstven': request.session['jedinstveni_broj_osiguranika']})

def promenaLicniPodaciPacijent(request):
    if request.method == 'POST':
        if (request.session['lokacija'] == 1):
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
            pacijent = Pacijent.objects.get(email_adresa=request.session['email'])
            if (request.POST.get('ime2', "") != ""):
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
            pacijent.save()
            return render(request, 'pacijent/glavnaStranicaPacijent.html',
                          {'email': request.session['email'], 'ime': request.session['ime'],
                           'prezime': request.session['prezime'], 'lokacija': request.session['lokacija'],
                           'lozinka': request.session['lozinka'], 'adresa': request.session['adresa_prebivalista'],
                           'grad': request.session['grad'], 'drzava': request.session['drzava'],
                           'broj': request.session['broja_telefona'],
                           'jedinstven': request.session['jedinstveni_broj_osiguranika']})
    else:
        # request.session['lokacija'] = 1.5
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
                       'krvna': request.session['krvna_grupa'],
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
                       'krvna': request.session['krvna_grupa'], 'lokacija': request.session['lokacija']
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
        if (pretrazuje == "naziv"):
            klinike = Klinika.objects.filter(naziv__icontains=sadrzaj)
        else:
            klinike = Klinika.objects.filter(opis__icontains=sadrzaj)
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
        lekari = Lekar.objects.filter(radno_mesto=naziv[3])
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
        pregledi = Pregled.objects.filter(klinika=naziv[4], zakazan="Prazno", vreme__gte=datetime.datetime.now())
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

        pregledi = Pregled.objects.filter(klinika=request.session['nazivKlinike'], zakazan="Prazno",
                                          vreme__gte=datetime.datetime.now())
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
                      {'lokacija': request.session['lokacija'], 'pregledi': pregledi, 'lekari': lekari})
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
        pregled = Pregled.objects.get(id=broj)
        pregled.zakazan = "Prazno"
        pregled.save()
        provera = datetime.datetime.now() - datetime.timedelta(days=1)
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


def sveOperacijePacijent(request):
    if request.method == 'POST':
        operacije = Operacije.objects.filter(pacijent=request.session['email']).order_by('-vreme')
        request.session['lokacija'] = 5

        lekari = Lekar.objects.all()
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'operacije': operacije, 'lekari': lekari})
    else:
        operacije = Operacije.objects.filter(pacijent=request.session['email']).order_by('-vreme')
        request.session['lokacija'] = 5

        lekari = Lekar.objects.all()
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'operacije': operacije, 'lekari': lekari})


def sortiranjeSveOperacijePacijent(request):
    if request.method == 'POST':
        if 'sortirajVreme' in request.POST:
            tip = 'vreme'
        elif 'sortirajKlinika' in request.POST:
            tip = 'klinika'
        elif 'sortirajSala' in request.POST:
            tip = 'sala'
        elif 'sortirajLekari' in request.POST:
            tip = 'lekari'
        else:
            tip = 'tip_operacije'

        operacije = Operacije.objects.filter(pacijent=request.session['email']).order_by(tip)
        lekari = Lekar.objects.all()
        request.session['lokacija'] = 5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'operacije': operacije, 'lekari': lekari})
    else:
        if 'sortirajVreme' in request.POST:
            tip = 'vreme'
        elif 'sortirajKlinika' in request.POST:
            tip = 'klinika'
        elif 'sortirajSala' in request.POST:
            tip = 'sala'
        elif 'sortirajLekari' in request.POST:
            tip = 'lekari'
        else:
            tip = 'tip_operacije'

        operacije = Operacije.objects.filter(pacijent=request.session['email']).order_by(tip)
        lekari = Lekar.objects.all()
        request.session['lokacija'] = 5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'operacije': operacije, 'lekari': lekari})


def zakazivanjePregledaPacijent(request):
    if request.method == 'POST':
        email = request.POST['kojiLekar']
        lekar = Lekar.objects.get(email_adresa=email)
        sale = Sala.objects.filter(id_klinike_kojoj_pripada=request.session['nazivKlinike'])
        return render(request, 'pacijent/zakazivanjePregledaPacijent.html',
                      {'lekar': lekar, 'sale': sale})
    else:
        return render(request, 'pacijent/zakazivanjePregledaPacijent.html',
                      )


def posaljiPregledPacijent(request):
    if request.method == 'POST':
        vreme = request.POST['vreme']
        zbog = request.POST['radi']
        kojiLekar = request.POST['kojiLekar']
        kojaSala = request.POST['kojasala']
        pregledi = Pregled.objects.all()
        max = -1

        for pregled in pregledi:
            if (max < int(pregled.id)):
                max = int(pregled.id)

        if (max == -1):
            max = 1
        else:
            max = max + 1

        pregled = Pregled.objects.create(klinika=request.session['nazivKlinike'], zakazan=request.session['email'],
                                         lekar=kojiLekar, sala=kojaSala, tip_pregleda=zbog, vreme=vreme,
                                         sifra_bolesti="Prazno", diagnoza="Prazno", lekovi="Prazno",
                                         id=max, prihvacen="ne")
        pregled.save()
        lekari = Lekar.objects.filter(radno_mesto=request.session['nazivKlinike'])
        request.session['lokacija'] = 3.5
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija'], 'lekari': lekari})
    else:
        return render(request, 'pacijent/glavnaStranicaPacijent.html',
                      {'lokacija': request.session['lokacija']})