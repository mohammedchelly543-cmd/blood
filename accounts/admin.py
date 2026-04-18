from django.contrib import admin
from .models import Donneur, Hopital

@admin.register(Donneur)
class DonneurAdmin(admin.ModelAdmin):
    list_display = ['user', 'groupe_sanguin', 'sexe', 'ville', 'actif']
    list_filter = ['groupe_sanguin', 'sexe', 'actif']

@admin.register(Hopital)
class HopitalAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'valide']
    list_filter = ['valide']
    actions = ['valider_hopital']

    def valider_hopital(self, request, queryset):
        queryset.update(valide=True)
    valider_hopital.short_description = "Valider les hôpitaux sélectionnés"