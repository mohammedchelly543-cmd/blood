from django.db import models
from accounts.models import Donneur, Hopital, GROUPES_SANGUINS

COMPATIBILITE = {
    'O-':  ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
    'O+':  ['O+', 'A+', 'B+', 'AB+'],
    'A-':  ['A-', 'A+', 'AB-', 'AB+'],
    'A+':  ['A+', 'AB+'],
    'B-':  ['B-', 'B+', 'AB-', 'AB+'],
    'B+':  ['B+', 'AB+'],
    'AB-': ['AB-', 'AB+'],
    'AB+': ['AB+'],
}

class DemandeUrgente(models.Model):
    STATUT_CHOICES = [
        ('active', 'Active'),
        ('cloturee', 'Clôturée'),
        ('satisfaite', 'Satisfaite'),
    ]

    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE, related_name='demandes')
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPES_SANGUINS)
    quantite = models.PositiveIntegerField(help_text='Nombre de poches')
    delai = models.DateField(help_text='Date limite')
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='active')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.groupe_sanguin} — {self.hopital.nom} ({self.statut})"

    @property
    def nb_reponses(self):
        return self.reponses.filter(statut='confirme').count()


class Don(models.Model):
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE, related_name='dons')
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE, related_name='dons_recus')
    date_don = models.DateField()
    notes = models.TextField(blank=True)
    valide = models.BooleanField(default=True)
    date_enregistrement = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_don']

    def __str__(self):
        return f"Don de {self.donneur} le {self.date_don}"


class ReponseAppel(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ]

    demande = models.ForeignKey(DemandeUrgente, on_delete=models.CASCADE, related_name='reponses')
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE, related_name='reponses')
    date_reponse = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        unique_together = ('demande', 'donneur')

    def __str__(self):
        return f"{self.donneur} → {self.demande}"