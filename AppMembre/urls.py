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

    # Cotisation et paiement
    path('cotisations/<int:cotisation_id>/payer',payerCotisation,name="payer_cotisation"),
    path('cotisation/',gestionCotisation,name="gestion_cotisation"),
    path('cotisation/nouvelle',creerCotisations,name='creer_cotisations'),
    path('cotisation/valdations_paiement//<int:paiement_id>/', changer_statut_paiement, name='changer_statut_paiement')

    # path('cotisations/ajouter/', ajouter_cotisation, name='ajouter_cotisation'),
    # path('cotisations/', liste_cotisations, name='liste_cotisations'),

    
    # path('membres/<int:pk>/cotisations/',gestion_cotisations, name='gestion_cotisations'),
]
