from django.urls import path
from .views import *

urlpatterns = [
    path('Blog',listeArticle,name='listeArticle'),
    path('Blog/<int:form_id>/',detail_article,name='detail_article'),
    path('ajout_blog',creer_article,name='creer_article')
]