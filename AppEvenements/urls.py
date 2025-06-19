from django.urls import path
from .views import *

urlpatterns = [
    path('evenement/',listEvenement,name='evenements'),
    path('ajout_evenement',creer_evenement,name='creer_evenement')
]