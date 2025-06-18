from django.urls import path
from .views import *

urlpatterns = [
    path('evenement',listEvenement,name='listEvenement'),
]