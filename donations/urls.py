from django.urls import path
from . import views

urlpatterns = [
    path('demandes/', views.liste_demandes, name='liste_demandes'),
    path('demandes/creer/', views.creer_demande, name='creer_demande'),
    path('demandes/<int:pk>/modifier/', views.modifier_demande, name='modifier_demande'),
    path('demandes/<int:pk>/cloturer/', views.cloturer_demande, name='cloturer_demande'),
    path('demandes/<int:pk>/repondre/', views.repondre_demande, name='repondre_demande'),
    path('dons/enregistrer/', views.enregistrer_don, name='enregistrer_don'),
    path('dons/historique/', views.historique_dons, name='historique_dons'),
]