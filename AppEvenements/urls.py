from django.urls import path
from .views import *

urlpatterns = [
    path('evenement/',listEvenement,name='evenements'),
    path('ajout_evenement',creer_evenement,name='creer_evenement'),
    path('detail_evenement/<int:form_id>/',detail_evenement,name='detail_evenement'),

    path('activite/',listActivites,name='activites'),
    path('ajout_activite',creer_activite,name='creer_activite'),
    path('detail_activite/<int:form_id>/',detail_activite,name='detail_activite'),
]