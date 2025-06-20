from django.shortcuts import render
from django.utils import timezone,timesince
from AppMembre.models import Utilisateur
from AppEquipe.models import Temoignage,Equipe
from AppActualite.models import*
from AppEvenements.models import Evenement,Activite

# Create your views here.
def accueilpage(request):
    # Dernières actualités (3 max)
    actualites = Actualite.objects.all().order_by('-date_publication')[:3]
    
    # Prochains événements (3 max)
    evenements = Evenement.objects.filter(
        date_debut__gte=timezone.now()
    ).order_by('date_debut')[:3]
    
    # Prochaines activités (3 max)
    activites = Activite.objects.filter(
        date_activites__gte=timezone.now()
    ).order_by('date_activites')[:3]
    
    # Derniers témoignages (3 max)
    temoignages = Temoignage.objects.filter(
        approuve=True
    ).order_by('-date_creation')[:3]
    
    context = {
        'actualites': actualites,
        'evenements': evenements,
        'activites': activites,
        'temoignages': temoignages,
        'session': request.session  # Pour vérifier la connexion
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