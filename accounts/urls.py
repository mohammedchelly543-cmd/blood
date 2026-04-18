from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.connexion, name='login'),
    path('accounts/logout/', views.deconnexion, name='logout'),
    path('accounts/register/donneur/', views.inscription_donneur, name='register_donneur'),
    path('accounts/register/hopital/', views.inscription_hopital, name='register_hopital'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/donneur/', views.dashboard_donneur, name='dashboard_donneur'),
    path('dashboard/hopital/', views.dashboard_hopital, name='dashboard_hopital'),
    path('accounts/dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('accounts/valider-hopital/<int:hopital_id>/', views.valider_hopital, name='valider_hopital'),
    path('accounts/export-csv/', views.export_donneurs_csv, name='export_donneurs_csv'),
]