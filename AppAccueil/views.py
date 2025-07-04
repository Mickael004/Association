from django.shortcuts import render
from django.utils import timezone,timesince
from AppMembre.models import Utilisateur
from AppEquipe.models import Temoignage,Equipe
from AppActualite.models import*
from AppEvenements.models import Evenement,Activite

from django.db.models import Q, Prefetch

# Create your views here.
def accueilpage(request):
    
    actualites = Actualite.objects.filter(etat='publie').prefetch_related(
        Prefetch('images',queryset=ImageActualite.objects.order_by('ordre'))
    ).order_by('-date_publication')
    
    
    evenements = Evenement.objects.filter(
        date_debut__gte=timezone.now()
    ).order_by('date_debut')
    
    
    activites = Activite.objects.filter(
        date_activites__gte=timezone.now()
    ).order_by('date_activites')
    
    
    temoignages = Temoignage.objects.filter(
        approuve=True
    ).order_by('-date_creation')[:3]
    
    context = {
        'actualites': actualites,
        'evenements': evenements,
        'activites': activites,
        'temoignages': temoignages,
        'session': request.session 
    }
    return render(request,'Accueil.html',context)

def aproposPage (request):
    equipe =Equipe.objects.all().order_by('ordre_affichage')
    temoignage = Temoignage.objects.filter(approuve=True).order_by('date_creation')

    context = {
        'equipe':equipe,
        'temoignage':temoignage
    }

    return render(request,'Apropos.html',context)