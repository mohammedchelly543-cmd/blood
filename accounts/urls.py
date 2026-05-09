from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('register/donneur/', views.inscription_donneur, name='register_donneur'),
    path('register/hopital/', views.inscription_hopital, name='register_hopital'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/donneur/', views.dashboard_donneur, name='dashboard_donneur'),
    path('dashboard/hopital/', views.dashboard_hopital, name='dashboard_hopital'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('valider-hopital/<int:hopital_id>/', views.valider_hopital, name='valider_hopital'),
    path('export-csv/', views.export_donneurs_csv, name='export_donneurs_csv'),
]