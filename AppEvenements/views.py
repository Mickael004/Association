from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from django.utils import timezone
from AppMembre.models import Utilisateur

# Create your views here.


def listEvenement(request):
    filtre = request.GET.get('filtre','tout')

    aujourdhui = timezone.now()
    evenements = Evenement.objects.all()

    if filtre == 'prochainement':
        evenements = evenements.filter(date_debut__gt=aujourdhui).order_by('date_debut')
    elif filtre == 'en_cours':
        evenements = evenements.filter(date_debut__lte=aujourdhui, date_fin__gt = aujourdhui).order_by('date_debut')
    elif filtre == 'termines':
        evenements = evenements.filter(date_fin__lte=aujourdhui).order_by('date_debut')

    else:
        evenements = evenements.order_by('date_debut')

    context = {
        'evenements':evenements,
        'filtre_actif':filtre,
        'aujourdhui':aujourdhui
    }

    return render(request,'Evenement.html',context)

# detail Evenement et Participation
def detail_evenement(request,form_id):
    evenement = get_object_or_404(Evenement, id=form_id)
    maintenant = timezone.now()

    # status
    if evenement.date_debut > maintenant:
        statut = "À venir"
        badge_class = "bg-info"
    elif evenement.date_fin < maintenant:
        statut = "Terminé"
        badge_class = "bg-secondary"
    else:
        statut = "En cours"
        badge_class = "bg-success"

    # verification inscrit
    est_inscrit = False
    if request.session.get('membres'):
        est_inscrit = evenement.nombre_participants.filter(
            id = request.session['membres']['id']
        ).exists()

    # Gestion participant
    if request.method == 'POST' and 'action' in request.POST:
        if request.session.get('membres'):

            utilisateur = Utilisateur.objects.get(id = request.session['membres']['id'])

            if request.POST['action'] == 'participer' :

                if(evenement.nombre_participant_max and evenement.nombre_participants.count()>= evenement.nombre_participant_max):
                    messages.error(request,"Desole l'evenement est complet")

                else:
                    # evenement.nombre_participants.add(utilisateur)
                    ParticipationEvenement.objects.get_or_create(
                    evenement=evenement,
                    participant=utilisateur
                )
                messages.success(request, "Vous êtes maintenant inscrit à cet événement")
            
            elif request.POST['action'] == 'annuler' :
                # evenement.nombre_participants.remove(utilisateur)

                ParticipationEvenement.objects.filter(
                    evenement=evenement,
                    participant=utilisateur
                ).delete()
                messages.success(request, "Votre participation a été annulée")
        
            return redirect('detail_evenement', form_id=form_id)

        else :
            messages.error(request, "Vous devez être connecté pour participer")
            return redirect('connexion')
    

    context = {
        'evenement': evenement,
        'statut': statut,
        'badge_class': badge_class,
        'est_inscrit': est_inscrit,
        'maintenant': maintenant,
        'membre': request.session.get('membres', {})
    }

    return render(request, 'EvenementDetail.html', context)

# insertion imqge
def inserer_photo(request,titre):
    if request.FILES.get("photo"):
        image = request.FILES.get("image")
        #Enregistrement avec nom unique
        with open(f"static/images/evenements/{titre}.jpg","wb") as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        return f"{titre}.jpg"
    

    

def creer_evenement(request):
    if request.session.get('membres',{}).get('role') in ['admin','moderateur']:
        if request.method == 'POST':
            titre = request.POST.get('titre')
            description = request.POST.get('description')
            date_debut = request.POST.get('date_debut')
            date_fin = request.POST.get('date_fin')
            lieu = request.POST.get('lieu')
            nombre_participant_max = request.POST.get('nombre_participant_max')
            # nom imqge
            nom_image = f"{titre}_{date_debut}"

            try : 
                createur = Utilisateur.objects.get(id= request.session['membres']['id'])

                nombre_max = int(nombre_participant_max) if nombre_participant_max else None
                evenements = Evenement(
                    titre=titre,
                    description=description,
                    date_debut=date_debut,
                    date_fin=date_fin,
                    lieu=lieu,
                    nombre_participant_max = nombre_max,
                    createur=createur,
                )

                if'image' in request.FILES:
                    evenements.image = request.FILES['image']
                evenements.save()
                messages.success(request,'Evenement Creer avec succes')
                return redirect('evenements')
            
            except Exception as e :
                messages.error(request, f"Une erreur est survenue: {str(e)}")
                return redirect('evenements')

    else:
        messages.error(request, "Accès réserver au Administrateur.")
        return redirect('accueil')
        
    context = {
        'membre' : request.session.get('membres')
    }

    return render(request,'EvenementCreer.html',context)



# Participation Evenement

def participer_evenement(request,form_id):
    evenement = get_object_or_404(Evenement, form_id=form_id)

    if evenement.participants.filter(id=request.session['membres']['id']).exists():
        evenement.participants.remove(Utilisateur.id)






# ################ ACTIVITES ################

def listActivites(request):
    
    activite_tous = Activite.objects.all().order_by('-date_creation')

    pass