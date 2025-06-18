from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from django.utils import timezone
from AppMembre.models import Utilisateur

# Create your views here.


def listEvenement(request):
    date_aujour = timezone.now()
    evenement_tous = Evenement.objects.all().order_by('-date_creation')
    evenement_a_venir = Evenement.objects.filter(date_debut__gte = date_aujour).order_by('-date_creation')
    evenement_passe = Evenement.objects.filter(date_debut__lt = date_aujour).order_by('-date_creation')

    context = {
        'evenements_venir' : evenement_a_venir,
        'evenement_passer':evenement_passe,
        'evenement_tous' : evenement_tous
    }
    return render(request,'Evenement.html',context)

# detail
def detail_evenement(request,form_id):
    evenement = Evenement.objects.get(id=form_id)

    context = {
        'detail_evenement':evenement
    }

    return render(request,'DetailEvenement.html')

# insertion imqge
def inserer_photo(request,titre):
    if request.FILES.get("photo"):
        image = request.FILES.get("image")
        #Enregistrement avec nom unique
        with open(f"static/images/evenements/{titre}.jpg","wb") as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        return f"{titre}.jpg"
    

# creer Evenement
def creer_evenement(request):
    if request.session.get('membres'):
        if request.session['membres']['role'] in ['administrateur','moderateur']:
            if request.method == 'POST':
                titre = request.POST.get('nom')
                description = request.POST.get('description')
                date_debut = request.POST.get('date_debut')
                date_fin = request.POST.get('date_fin')
                lieu = request.POST.get('lieu')
                image = request.POST.get('image')
                participants = request.POST.get('participants')
                createur = request.session['membres']['id']

                statut = request.POST.get('statut')
                # nom imqge
                nom_image = f"{titre}_{date_debut}"

                evenements = Evenement(
                    titre=titre,
                    description=description,
                    date_debut=date_debut,
                    date_fin=date_fin,
                    lieu=lieu,
                    image=f"static/images/evenemets/{inserer_photo(request,nom_image)}",
                    statut = statut,
                    createur=createur,
                    participants=participants
                )
                evenements.save()
                messages.success(request,'Evenement Creer avec succes')
                return redirect('listEvenement')

        else:
            messages.error(request, "Accès non autorisé.")
            return redirect('accueil')



# Participation Evenement

def participer_evenement(request,form_id):
    evenement = get_object_or_404(Evenement, form_id=form_id)

    if evenement.participants.filter(id=request.session['membres']['id']).exists():
        evenement.participants.remove(Utilisateur.id)






# ################ ACTIVITES ################

def listActivites(request):
    
    activite_tous = Activite.objects.all().order_by('-date_creation')

    pass