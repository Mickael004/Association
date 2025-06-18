from django.urls import path
from .views import *

urlpatterns = [
    path('',accueilpage,name='accueil'),
    path(r'apropos/',aproposPage,name='aproposPage'),

]