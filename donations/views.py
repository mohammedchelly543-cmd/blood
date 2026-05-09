from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import donneur_required, hopital_required
from .models import DemandeUrgente, Don, ReponseAppel
from accounts.models import Donneur, Hopital, COMPATIBILITE
from datetime import date


def liste_demandes(request):
    demandes = DemandeUrgente.objects.filter(statut='active').order_by('delai')
    groupe_filtre = request.GET.get('groupe', '')
    if groupe_filtre:
        demandes = demandes.filter(groupe_sanguin=groupe_filtre)
    return render(request, 'donations/liste_demandes.html', {
        'demandes': demandes,
        'groupe_filtre': groupe_filtre,
        'groupes': ['A+','A-','B+','B-','AB+','AB-','O+','O-'],
    })


@hopital_required
def creer_demande(request):
    from .forms import DemandeUrgenteForm
    hopital = request.user.hopital
    if request.method == 'POST':
        form = DemandeUrgenteForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.hopital = hopital
            demande.save()
            messages.success(request, 'Demande urgente publiée.')
            return redirect('dashboard_hopital')
    else:
        form = DemandeUrgenteForm()
    return render(request, 'donations/creer_demande.html', {'form': form})


@hopital_required
def modifier_demande(request, pk):
    from .forms import DemandeUrgenteForm
    demande = get_object_or_404(DemandeUrgente, pk=pk, hopital=request.user.hopital)
    if request.method == 'POST':
        form = DemandeUrgenteForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            messages.success(request, 'Demande modifiée.')
            return redirect('dashboard_hopital')
    else:
        form = DemandeUrgenteForm(instance=demande)
    return render(request, 'donations/creer_demande.html', {'form': form, 'modifier': True})


@hopital_required
def cloturer_demande(request, pk):
    demande = get_object_or_404(DemandeUrgente, pk=pk, hopital=request.user.hopital)
    demande.statut = 'cloturee'
    demande.save()
    messages.success(request, 'Demande clôturée.')
    return redirect('dashboard_hopital')


@donneur_required
def repondre_demande(request, pk):
    demande = get_object_or_404(DemandeUrgente, pk=pk, statut='active')
    donneur = request.user.donneur
    if not donneur.est_eligible():
        messages.warning(request, f'Vous ne pouvez pas donner avant le {donneur.prochain_don().strftime("%d/%m/%Y")}.')
        return redirect('liste_demandes')
    _, created = ReponseAppel.objects.get_or_create(demande=demande, donneur=donneur)
    if created:
        messages.success(request, 'Votre réponse a été enregistrée. L\'hôpital vous contactera.')
    else:
        messages.info(request, 'Vous avez déjà répondu à cet appel.')
    return redirect('liste_demandes')


@donneur_required
def enregistrer_don(request):
    donneur = request.user.donneur
    if request.method == 'POST':
        hopital_id = request.POST.get('hopital')
        date_don = request.POST.get('date_don')
        notes = request.POST.get('notes', '')
        hopital = get_object_or_404(Hopital, id=hopital_id, valide=True)
        Don.objects.create(donneur=donneur, hopital=hopital,
                           date_don=date_don, notes=notes)
        messages.success(request, 'Don enregistré avec succès !')
        return redirect('dashboard_donneur')
    hopitaux = Hopital.objects.filter(valide=True)
    return render(request, 'donations/enregistrer_don.html', {
        'hopitaux': hopitaux,
        'today': date.today().strftime('%Y-%m-%d'),
    })


@donneur_required
def historique_dons(request):
    dons = Don.objects.filter(donneur=request.user.donneur).order_by('-date_don')
    return render(request, 'donations/historique_dons.html', {'dons': dons})