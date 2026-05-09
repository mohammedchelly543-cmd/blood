from django.db import models
from django.contrib.auth.models import User

GROUPES_SANGUINS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

# ✅ AJOUT IMPORTANT
COMPATIBILITE = {
    'O-': ['O-','O+','A-','A+','B-','B+','AB-','AB+'],
    'O+': ['O+','A+','B+','AB+'],
    'A-': ['A-','A+','AB-','AB+'],
    'A+': ['A+','AB+'],
    'B-': ['B-','B+','AB-','AB+'],
    'B+': ['B+','AB+'],
    'AB-': ['AB-','AB+'],
    'AB+': ['AB+'],
}


class Donneur(models.Model):
    SEXE_CHOICES = [('M', 'Homme'), ('F', 'Femme')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donneur')
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPES_SANGUINS)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField()
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    actif = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.groupe_sanguin}"

    @property
    def prochain_don(self):
        from donations.models import Don
        from datetime import timedelta

        dernier = Don.objects.filter(donneur=self, valide=True)\
                             .order_by('-date_don').first()
        if not dernier:
            return None

        jours = 56 if self.sexe == 'M' else 84
        return dernier.date_don + timedelta(days=jours)

    @property
    def est_eligible(self):
        from datetime import date

        prochain = self.prochain_don
        if not prochain:
            return True
        return date.today() >= prochain


class Hopital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hopital')
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=300)
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    numero_agrement = models.CharField(max_length=100, unique=True)
    valide = models.BooleanField(default=False)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom