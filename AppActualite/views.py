from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Actualite,Commentaire
from django.utils import timezone,timesince
from AppMembre.models import Utilisateur

import os
from django.conf import settings
from django.core.files.storage import default_storage
# Create your views here.

def listActualite(request):
    actualites = Actualite.objects.all().order_by('-date_publication')

    return render(request,'Actualite.html',{'actualites':actualites})


def inserer_photo(request, titre):
    if 'image' in request.FILES:
        image = request.FILES['image']
        nom_fichier = f"{titre.replace(' ', '_')}_{image.name}"
        chemin_relatif = os.path.join('images/actualites', nom_fichier)
        
        
        chemin_absolu = os.path.join(settings.MEDIA_ROOT, 'images/actualites', nom_fichier)
        
        
        os.makedirs(os.path.dirname(chemin_absolu), exist_ok=True)
        
        
        with default_storage.open(chemin_absolu, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        return chemin_relatif 
    

def creer_actualite(request):
    if not request.session.get('membres', {}).get('role') in ['admin', 'moderateur','membre']:
        messages.error(request, "Accès réservé aux administrateurs")
        return redirect('accueil')

    titre = request.POST.get('titre')
    contenue = request.POST.get('contenue')
    date = timezone.now().date()
    nom_image = f"{titre}_{date}"
    if request.method == 'POST':
        try:

            auteur = Utilisateur.objects.get(id=request.session['membres']['id'])

            if not titre or not contenue:
                messages.error(request, "Le titre et le contenu sont obligatoires")
                return render(request, 'ActualiteCreer.html', {
                    'titre': titre,
                    'contenue': contenue,
                    'membre': request.session.get('membres')
                })


            if 'image' in request.FILES:
                
                chemin_image = inserer_photo(request,nom_image)
                actualite = Actualite(
                    auteur=auteur,
                    titre=titre,
                    contenue=contenue,
                    image=chemin_image
                )

                actualite.save()
                messages.success(request, "Actualité créée avec succès !")
                return redirect('actualite')

        except Exception as e:
            messages.error(request, f"Une erreur est survenue: {str(e)}")
            return render(request, 'ActualiteCreer.html', {
                'titre': titre,
                'contenue': contenue,
                'membre': request.session.get('membres')
            })

    return render(request, 'ActualiteCreer.html', {
        'membre': request.session.get('membres')
    })


def ajouter_commentaire(request, form_id):
    actualite = get_object_or_404(Actualite,id=form_id)
    if not request.session.get('membres'):
        messages.error(request, "Vous devez être connecté pour commenter")
        return redirect('connexionPage')

    if request.method == 'POST':
        message = request.POST.get('message')
        auteur = Utilisateur.objects.get(id=request.session['membres']['id'])
        if not message:
            messages.error(request, "Le commentaire ne peut pas être vide")
            return redirect('actualite')

        try:
            Commentaire.objects.create(
                actualite=actualite,
                auteur=auteur,
                message=message
            )
            messages.success(request, "Commentaire ajouté !")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")

    return redirect('actualite')

def get_commentaires(request, form_id):
    actualite = get_object_or_404(Actualite, id=form_id)
    commentaires = Commentaire.objects.filter(actualite=actualite).order_by('date_commentaire')
    return render(request, 'ActualiteModalCommentaire.html', {'commentaires': commentaires})