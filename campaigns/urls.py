from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_campagnes, name='liste_campagnes'),
    path('creer/', views.creer_campagne, name='creer_campagne'),
    path('<int:pk>/', views.detail_campagne, name='detail_campagne'),
    path('<int:pk>/inscrire/', views.inscrire_campagne, name='inscrire_campagne'),
]