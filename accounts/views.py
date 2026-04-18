from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InscriptionDonneurForm, InscriptionHopitalForm
from .models import Donneur, Hopital
from .decorators import donneur_required, hopital_required, admin_required
from django.http import HttpResponse
import csv


def home(request):
    return render(request, 'home.html')


def inscription_donneur(request):
    if request.method == 'POST':
        form = InscriptionDonneurForm(request.POST)
        if form.is_valid():
            # Créer le User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            # Créer le Donneur lié
            donneur = form.save(commit=False)
            donneur.user = user
            donneur.save()
            messages.success(request, 'Compte créé avec succès ! Vous pouvez vous connecter.')
            return redirect('login')
    else:
        form = InscriptionDonneurForm()
    return render(request, 'accounts/register_donneur.html', {'form': form})


def inscription_hopital(request):
    if request.method == 'POST':
        form = InscriptionHopitalForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            hopital = form.save(commit=False)
            hopital.user = user
            hopital.save()
            messages.success(request, 'Demande envoyée ! Votre compte sera validé par un administrateur.')
            return redirect('login')
    else:
        form = InscriptionHopitalForm()
    return render(request, 'accounts/register_hopital.html', {'form': form})


def connexion(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'accounts/login.html')


def deconnexion(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    user = request.user
    if user.is_staff:
        return redirect('dashboard_admin')
    elif hasattr(user, 'donneur'):
        return redirect('dashboard_donneur')
    elif hasattr(user, 'hopital'):
        return redirect('dashboard_hopital')
    return redirect('home')


@donneur_required
def dashboard_donneur(request):
    donneur = request.user.donneur
    from donations.models import Don, DemandeUrgente, ReponseAppel
    from accounts.models import COMPATIBILITE

    dons = Don.objects.filter(donneur=donneur).order_by('-date_don')[:5]
    groupes_compatibles = COMPATIBILITE.get(donneur.groupe_sanguin, [])
    demandes = DemandeUrgente.objects.filter(
        statut='active',
        groupe_sanguin__in=groupes_compatibles
    ).order_by('delai')[:5]

    context = {
        'donneur': donneur,
        'dons': dons,
        'demandes': demandes,
        'eligible': donneur.est_eligible(),
        'prochain_don': donneur.prochain_don(),
    }
    return render(request, 'accounts/dashboard_donneur.html', context)


@hopital_required
def dashboard_hopital(request):
    hopital = request.user.hopital
    from donations.models import DemandeUrgente
    from campaigns.models import Campagne

    demandes = DemandeUrgente.objects.filter(hopital=hopital).order_by('-date_creation')
    campagnes = Campagne.objects.filter(hopital=hopital).order_by('-date')

    context = {
        'hopital': hopital,
        'demandes': demandes,
        'campagnes': campagnes,
    }
    return render(request, 'accounts/dashboard_hopital.html', context)


@admin_required
def dashboard_admin(request):
    from donations.models import Don, DemandeUrgente
    from campaigns.models import Campagne

    context = {
        'nb_donneurs': Donneur.objects.filter(actif=True).count(),
        'nb_hopitaux': Hopital.objects.filter(valide=True).count(),
        'nb_hopitaux_attente': Hopital.objects.filter(valide=False).count(),
        'nb_dons': Don.objects.count(),
        'demandes_actives': DemandeUrgente.objects.filter(statut='active').order_by('delai'),
        'hopitaux_attente': Hopital.objects.filter(valide=False),
    }
    return render(request, 'accounts/dashboard_admin.html', context)
@admin_required
def valider_hopital(request, hopital_id):
    hopital = Hopital.objects.get(id=hopital_id)
    hopital.valide = True
    hopital.save()
    messages.success(request, f'Hôpital "{hopital.nom}" validé avec succès.')
    return redirect('dashboard_admin')


@admin_required
def export_donneurs_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="donneurs.csv"'
    response.write('\ufeff')  # BOM pour Excel

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Nom', 'Prénom', 'Email', 'Groupe sanguin', 'Sexe',
                     'Date naissance', 'Ville', 'Téléphone', 'Actif', 'Inscrit le'])

    for d in Donneur.objects.select_related('user').all():
        writer.writerow([
            d.user.last_name,
            d.user.first_name,
            d.user.email,
            d.groupe_sanguin,
            d.get_sexe_display(),
            d.date_naissance.strftime('%d/%m/%Y'),
            d.ville,
            d.telephone,
            'Oui' if d.actif else 'Non',
            d.date_inscription.strftime('%d/%m/%Y'),
        ])
    return response