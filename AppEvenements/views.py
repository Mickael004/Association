from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from django.utils import timezone,timesince
from AppMembre.models import Utilisateur

import os
from django.conf import settings
from django.core.files.storage import default_storage
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
    if request.method == 'POST':
        if 'action' in request.POST:
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
            
        elif 'publier_actu' in request.POST and request.session.get('membres', {}).get('role') in ['admin', 'moderateur']:
            return redirect('creer_actualite_liee',
                            type_objet='evenement',
                             objet_id=evenement.id)
    

    context = {
        'evenement': evenement,
        'statut': statut,
        'badge_class': badge_class,
        'est_inscrit': est_inscrit,
        'maintenant': maintenant,
        'membre': request.session.get('membres', {}),
        'peut_publier_actu':request.session.get('membres', {}).get('role') in ['admin', 'moderateur']
    }

    return render(request, 'EvenementDetail.html', context)

# insertion imqge
def inserer_photo(request, titre):
    if 'image' in request.FILES:
        image = request.FILES['image']
        nom_fichier = f"{titre.replace(' ', '_')}_{image.name}.jpg"
        chemin_relatif = os.path.join('images/evenements', nom_fichier)
        
        
        chemin_absolu = os.path.join(settings.MEDIA_ROOT, 'images/evenements', nom_fichier)
        
        
        os.makedirs(os.path.dirname(chemin_absolu), exist_ok=True)
        
        
        with default_storage.open(chemin_absolu, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        return chemin_relatif  
       

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
                
                if'image' in request.FILES:
                    chemin_image = inserer_photo(request,nom_image)

                    evenements = Evenement(
                        titre=titre,
                        description=description,
                        date_debut=date_debut,
                        date_fin=date_fin,
                        lieu=lieu,
                        nombre_participant_max = nombre_max,
                        createur=createur,
                        image = chemin_image
                    )
                    evenements.save()
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





# ################ ACTIVITES ################

def listActivites(request):
    filtre = request.GET.get('filtre','tout')

    aujourdhui = timezone.now().date()
    heureauj = timezone.now().time()
    activites = Activite.objects.all()

    if filtre == 'prochainement':
        activites = activites.filter(date_activites__gt=aujourdhui).order_by('date_activites')
    elif filtre == 'termines':
        activites = activites.filter(date_activites__lte=aujourdhui).order_by('date_activites')

    else:
        activites = activites.order_by('date_activites')

    context = {
        'activites':activites,
        'filtre_actif':filtre,
        'aujourdhui':aujourdhui,
        'heureauj':heureauj
    }

    return render(request,'Activite.html',context)



def detail_activite(request,form_id):
    activite = get_object_or_404(Activite, id=form_id)
    maintenant = timezone.now().date()

    # status
    if activite.date_activites > maintenant:
        statut = "À venir"
        badge_class = "bg-info"
    # elif activite.date_fin < maintenant:
    #     statut = "Terminé"
    #     badge_class = "bg-secondary"
    else:
        statut = "Terminé"
        badge_class = "bg-secondary"
        # statut = "En cours"
        # badge_class = "bg-success"

    # verification inscrit
    est_inscrit = False
    if request.session.get('membres'):
        est_inscrit = ParticipationActivite.objects.filter(
            activite = activite,
            id = request.session['membres']['id']
        ).exists()

    # Gestion participant
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.session.get('membres'):

                utilisateur = Utilisateur.objects.get(id = request.session['membres']['id'])

                if request.POST['action'] == 'participer' :

                    
                        # evenement.nombre_participants.add(utilisateur)
                    ParticipationActivite.objects.get_or_create(
                    activite=activite,
                    participant=utilisateur
                    )
                    messages.success(request, "Vous êtes maintenant inscrit à cet activite")
                
                elif request.POST['action'] == 'annuler' :
                    # evenement.nombre_participants.remove(utilisateur)

                    ParticipationActivite.objects.filter(
                        activite=activite,
                        participant=utilisateur
                    ).delete()
                    messages.success(request, "Votre participation a été annulée")
            
                return redirect('detail_activite', form_id=form_id)

            else :
                messages.error(request, "Vous devez être connecté pour participer")
                return redirect('connexion')
            
        elif 'publier_actu' in request.POST and request.session.get('membres', {}).get('role') in ['admin', 'moderateur']:
            return redirect('creer_actualite_liee',
                            type_objet='activite',
                            objet_id= activite.id)
    

    context = {
        'activite': activite,
        'statut': statut,
        'badge_class': badge_class,
        'est_inscrit': est_inscrit,
        'maintenant': maintenant,
        'membre': request.session.get('membres', {}),
        'peut_publier_actu':request.session.get('membres', {}).get('role') in ['admin', 'moderateur']
    }

    return render(request, 'ActiviteDetail.html', context)


def inserer_photo_activite(request, titre):
    if 'image' in request.FILES:
        image = request.FILES['image']
        nom_fichier = f"{titre.replace(' ', '_')}_{image.name}.jpg"
        chemin_relatif = os.path.join('images/activites', nom_fichier)
        
        
        chemin_absolu = os.path.join(settings.MEDIA_ROOT, 'images/activites', nom_fichier)
        
        
        os.makedirs(os.path.dirname(chemin_absolu), exist_ok=True)
        
        
        with default_storage.open(chemin_absolu, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        return chemin_relatif
    

def creer_activite(request):
    if request.session.get('membres',{}).get('role') in ['admin','moderateur']:
        if request.method == 'POST':
            nom = request.POST.get('nom')
            description = request.POST.get('description')
            date_activites = request.POST.get('date_activites')
            horaire_debut = request.POST.get('horaire_debut')
            horaire_fin = request.POST.get('horaire_fin')
            lieu = request.POST.get('lieu')
            # nom imqge
            nom_image = f"{nom}_{date_activites}"

            try : 
                createur = Utilisateur.objects.get(id= request.session['membres']['id'])

                if'image' in request.FILES:
                    chemin_image = inserer_photo_activite(request,nom_image)

                    activites = Activite(
                        nom=nom,
                        description=description,
                        date_activites=date_activites,
                        horaire_debut=horaire_debut,
                        horaire_fin=horaire_fin,
                        lieu=lieu,
                        createur=createur,
                        image = chemin_image
                    )
                    activites.save()
                    return redirect('activites')
            
            except Exception as e :
                messages.error(request, f"Une erreur est survenue: {str(e)}")
                return redirect('activites')

    else:
        messages.error(request, "Accès réserver au Administrateur.")
        return redirect('accueil')
        
    context = {
        'membre' : request.session.get('membres')
    }

    return render(request,'ActiviteCreer.html',context)