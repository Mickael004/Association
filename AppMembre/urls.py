from django.urls import path
from . import views

app_name = 'membres'

urlpatterns = [
    # Authentification
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    
    # Profil
    path('profil/', views.profil, name='profil'),
    path('profil/modifier/', views.edit_profil, name='edit_profil'),
    # path('profil/mot-de-passe/', views.change_password, name='change_password'),
    
    # Admin
    # path('membres/', views.liste_membres, name='liste_membres'),
    # path('membres/<int:pk>/', views.detail_membre, name='detail_membre'),
    # path('membres/<int:pk>/modifier/', views.edit_membre, name='edit_membre'),
    # path('membres/<int:pk>/cotisations/', views.gestion_cotisations, name='gestion_cotisations'),
]
