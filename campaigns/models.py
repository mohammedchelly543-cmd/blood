from django.db import models
from accounts.models import Hopital, Donneur, GROUPES_SANGUINS

class Campagne(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE, related_name='campagnes')
    nom = models.CharField(max_length=200)
    date = models.DateField()
    lieu = models.CharField(max_length=300)
    groupes_cibles = models.CharField(max_length=100, help_text='Ex: A+, O-, B+')
    capacite_totale = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} — {self.date}"

    def places_restantes(self):
        return self.capacite_totale - self.inscriptions.count()

    def est_complete(self):
        return self.places_restantes() <= 0


class Inscription(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, related_name='inscriptions')
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE, related_name='inscriptions')
    creneau_horaire = models.TimeField()
    date_inscription = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('campagne', 'donneur')

    def __str__(self):
        return f"{self.donneur} → {self.campagne.nom}"