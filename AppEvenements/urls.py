from django.urls import path
from .views import *

urlpatterns = [
    path('evenement/',listEvenement,name='evenements'),
    path('ajout_evenement',creer_evenement,name='creer_evenement'),
    path('detail_evenement/<int:form_id>/',detail_evenement,name='detail_evenement')
]