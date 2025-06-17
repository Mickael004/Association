from django.urls import path
from .views import accueilpage

urlpatterns = [
    path('',accueilpage,name='accueil')
]