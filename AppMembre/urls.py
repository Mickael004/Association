from django.urls import path
from .views import *


urlpatterns = [
    # Authentification
    path('connexion/',connexionPage,name='connexionPage'),
    path('connexion', connexion, name='connexion'),
    path('inscription/',inscriptionPage,name='inscriptionPage'),
    path('inscription',inscrire_membre, name='inscription'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    
    # Profil
    path('profil/', profil, name='profil'),
    # path('profil/modifier/', views.edit_profil, name='edit_profil'),
    # path('profil/mot-de-passe/', views.change_password, name='change_password'),
    
    # Admin
    # path('membres/', views.liste_membres, name='liste_membres'),
    # path('membres/<int:pk>/', views.detail_membre, name='detail_membre'),
    # path('membres/<int:pk>/modifier/', views.edit_membre, name='edit_membre'),
    # path('membres/<int:pk>/cotisations/', views.gestion_cotisations, name='gestion_cotisations'),
]
