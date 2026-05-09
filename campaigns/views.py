from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import donneur_required, hopital_required
from .models import Campagne, Inscription


def liste_campagnes(request):
    campagnes = Campagne.objects.order_by('-date')
    return render(request, 'campaigns/liste_campagnes.html', {'campagnes': campagnes})


@hopital_required
def creer_campagne(request):
    from .forms import CampagneForm
    if request.method == 'POST':
        form = CampagneForm(request.POST)
        if form.is_valid():
            campagne = form.save(commit=False)
            campagne.hopital = request.user.hopital
            campagne.save()
            messages.success(request, 'Campagne créée.')
            return redirect('dashboard_hopital')
    else:
        form = CampagneForm()
    return render(request, 'campaigns/creer_campagne.html', {'form': form})


def detail_campagne(request, pk):
    campagne = get_object_or_404(Campagne, pk=pk)
    inscriptions = campagne.inscriptions.all()
    return render(request, 'campaigns/detail_campagne.html', {
        'campagne': campagne,
        'inscriptions': inscriptions,
    })


@donneur_required
def inscrire_campagne(request, pk):
    campagne = get_object_or_404(Campagne, pk=pk)
    donneur = request.user.donneur
    if campagne.est_complete:
        messages.error(request, 'Cette campagne est complète.')
        return redirect('detail_campagne', pk=pk)
    creneau = request.POST.get('creneau_horaire')
    _, created = Inscription.objects.get_or_create(
        campagne=campagne, donneur=donneur,
        defaults={'creneau_horaire': creneau}
    )
    if created:
        messages.success(request, 'Inscription confirmée !')
    else:
        messages.info(request, 'Vous êtes déjà inscrit à cette campagne.')
    return redirect('detail_campagne', pk=pk)