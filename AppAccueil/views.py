from django.shortcuts import render
from AppMembre.models import Utilisateur
from AppEquipe.models import Temoignage,Equipe

# Create your views here.
def accueilpage(request):
    return render(request,'Accueil.html')

def aproposPage (request):
    equipe =Equipe.objects.all().order_by('ordre_affichage')
    temoignage = Temoignage.objects.filter(approuve=True).order_by('date_creation')

    context = {
        'equipe':equipe,
        'temoignage':temoignage
    }

    return render(request,'Apropos.html',context)