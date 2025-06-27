from django.urls import path
from .views import *

urlpatterns = [
    path('actualite/',listActualite,name='actualite'),
    path('actualite/<int:form_id>/commenter',ajouter_commentaire,name='ajouter_commentaire'),
    path('actualite/<int:form_id>/commentaires/',get_commentaires,name='get_commentaires'),
    path('ajout_actualite',creer_actualite,name='creer_actualite'),

    path('actualite/nouvelle/',creer_actualite_liee,name='creer_actualite'),
    path('actualite/nouvelle/<str:type_objet>/<int:objet_id>/',creer_actualite_liee,name='creer_actualite_liee')
]   