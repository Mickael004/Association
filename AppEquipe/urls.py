from django.urls import path
from .views import *

urlpatterns = [
    path('list_membres/',liste_membres,name="liste_membres"),
    path('equipe/ajouter/<int:membre_id>/', ajouter_equipe, name='ajouter_equipe'),
    path('equipe/retirer/<int:membre_id>/', retirer_equipe, name='retirer_equipe'),

    path('notre_equipe/',notre_equipe,name='notre_equipe'),
]