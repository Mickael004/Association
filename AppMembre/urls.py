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
    path('modification_profil',updateProfile, name='updateProfile'),
    path('modification_password',modif_mot_passe,name='modif_mot_passe'),


    path('cotisations/ajouter/', ajouter_cotisation, name='ajouter_cotisation'),
    path('cotisations/', liste_cotisations, name='liste_cotisations'),

    
    # path('membres/<int:pk>/cotisations/',gestion_cotisations, name='gestion_cotisations'),
]
