from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Actualite,Commentaire,ImageActualite
from django.utils import timezone,timesince
from AppMembre.models import Utilisateur
from AppEvenements.models import Evenement,Activite
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch


import os
from django.conf import settings
from django.core.files.storage import default_storage
# Create your views here.

def listActualite(request):
    # actualites = Actualite.objects.all().order_by('-date_publication')

    # return render(request,'Actualite.html',{'actualites':actualites})

    staff = request.session.get('membres', {}).get('role') in ['admin', 'moderateur']

    filtre_etat = request.GET.get('filter','publie')

    actualites = Actualite.objects.all().prefetch_related(
        Prefetch('images',queryset=ImageActualite.objects.order_by('ordre'))
    )


    if staff:
        if filtre_etat == 'publie':
            actualites = actualites.filter(etat='publie')

        elif filtre_etat == 'en_attente':
            actualites = actualites.filter(etat='en_attente')
        elif filtre_etat == 'brouillon':
            actualites = actualites.filter(etat='brouillon')
    else:
        # Pour les membres normaux, ne montrer que les publiés
        actualites = actualites.filter(etat='publie')

    # Pagination
    pagination = Paginator(actualites, 10)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    context = {
        'actualites': page_obj,
        'staff': staff,
        'filtre_etat': filtre_etat,
    }

    return render(request, 'actualites/Liste.html', context)


# ///////:Validation
def valider_publication(request, form_id):
    if request.session.get('membres', {}).get('role') not in ['admin', 'moderateur']:
        messages.error(request, "Vous n'avez pas les droits pour valider des publications")
        return redirect('liste_actualites')
    
    actualite = get_object_or_404(Actualite, id=form_id)
    actualite.etat = 'publie'
    actualite.save()
    
    messages.success(request, "L'actualité a été publiée avec succès!")
    return redirect('liste_actualites')



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

            actualite = Actualite(
                auteur=auteur,
                titre=titre,
                contenue=contenue,
            )

            actualite.save()

            if 'image' in request.FILES:
                
                chemin_image = inserer_photo(request,nom_image)
                for i, chemin_image in enumerate(request.FILES.getlist('images')):
                    ImageActualite.objects.create(
                        actualite=actualite,
                        image=inserer_photo(request,chemin_image),
                        ordre=i
                    )
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

# \\\\\\\\\\ Actualiter Creer avec lien /////

def creer_actualite_liee(request, type_objet=None, objet_id=None):
    # Vérification des permissions
    if not request.session.get('membres', {}).get('role') in ['admin', 'moderateur', 'membre']:
        messages.error(request, "Vous n'avez pas les droits pour publier une actualité")
        return redirect('accueil')
    
    # Initialisation des variables
    objet = None
    template_lien = ""
    titre_initial = "Nouvelle actualité"
    
    # Gestion des actualités liées
    if type_objet and objet_id:
        if type_objet == 'evenement':
            objet = get_object_or_404(Evenement, id=objet_id)
            template_lien = f"<a href='{reverse('detail_evenement', args=[objet.id])}' class='badge bg-info'>Événement: {objet.titre}</a>"
            titre_initial = f"Nouvelle actualité sur {objet.titre}"
        elif type_objet == 'activite':
            objet = get_object_or_404(Activite, id=objet_id)
            template_lien = f"<a href='{reverse('detail_activite', args=[objet.id])}' class='badge bg-success'>Activité: {objet.nom}</a>"
            titre_initial = f"Nouvelle actualité sur {objet.nom}"
    
    if request.method == 'POST':
        try:
            # Récupération de l'auteur
            auteur = Utilisateur.objects.get(id=request.session['membres']['id'])
            
            # Création de l'actualité
            actualite = Actualite(
                titre=request.POST.get('titre'),
                contenue=f"{request.POST.get('contenue')}<br><br>{template_lien}" if template_lien else request.POST.get('contenue'),
                auteur=auteur,
                etat='publie' if (request.POST.get('evenement') or request.POST.get('activite')) else 'en_attente'
            )
            
            # Liaison avec l'événement/activité
            if type_objet == 'evenement':
                actualite.evenement = objet
            elif type_objet == 'activite':
                actualite.activite = objet
            else:
                if request.POST.get('evenement'):
                    actualite.evenement_id = request.POST.get('evenement')
                if request.POST.get('activite'):
                    actualite.activite_id = request.POST.get('activite')
            
            actualite.save()
            
            # Gestion des images multiples
            if 'images' in request.FILES:
                for i, image in enumerate(request.FILES.getlist('images')):
                    ImageActualite.objects.create(
                        actualite=actualite,
                        image=image,
                        ordre=i
                    )
            
            messages.success(request, "Actualité publiée avec succès !" if actualite.etat == 'publie' else "Actualité soumise pour validation !")
            return redirect('detail_actualite', form_id=actualite.id)
        
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    # Préparation du contexte
    context = {
        'type_objet': type_objet,
        'objet_id': objet_id,
        'titre_initial': titre_initial,
        'objet': objet
    }
    
    # Ajout des listes pour le formulaire libre
    if not type_objet:
        context['evenements'] = Evenement.objects.filter(date_debut__gte=timezone.now())
        context['activites'] = Activite.objects.filter(date_activites=timezone.now())
    return render(request, 'actualites/CreerLiees.html',context)



# def creer_actualite_liee(request,type_objet,objet_id):
#     if not request.session.get('membres', {}).get('role') in ['admin', 'moderateur','membre']:
#         messages.error(request, "Vous n'avez pas les droits pour publier une actualité")
#         return redirect('accueil')
    
#     if type_objet == 'evenement':
#         objet = get_object_or_404(Evenement, id=objet_id)
#         template_lien = f"<a href='{reverse('detail_evenement', args=[objet.id])}' class='badge bg-info'>Événement: {objet.titre}</a>"
#     elif type_objet == 'activite':
#         objet = get_object_or_404(Activite, id=objet_id)
#         template_lien = f"<a href='{reverse('detail_activite', args=[objet.id])}' class='badge bg-success'>Activité: {objet.nom}</a>"
#     else:
#         messages.error(request, "Type d'objet inconnu")
#         return redirect('accueil')
    
#     if request.method == 'POST':
#         try:
#             auteur = Utilisateur.objects.get(id=request.session['membres']['id'])
#             actualite = Actualite(
#                 titre=request.POST.get('titre'),
#                 contenue=f"{request.POST.get('contenue')}<br><br>{template_lien}",
#                 auteur=auteur,
#                 etat='publie'
#             )
#             if type_objet == 'evenement':
#                 actualite.evenement = objet
#             else:
#                 actualite.activite = objet
            
#             actualite.save()

#             if 'image' in request.FILES:
#                 for i, image in enumerate(request.FILES.getlist('images')):
#                     ImageActualite.objects.create(
#                         actualite=actualite,
#                         image=inserer_photo(request,image),
#                         ordre=i
#                     )
#             messages.success(request, "Actualité publiée avec succès !")
#             return redirect('detail_actualite', form_id=actualite.id)
#         except Exception as e:
#             messages.error(request, f"Erreur: {str(e)}")
    
#     # Pré-remplir le titre avec le nom de l'événement/activité
#     titre_initial = f"Nouvelle actualité sur {objet.titre if type_objet == 'evenement' else objet.nom}"
    
#     return render(request, 'actualites/CreerLiees.html', {
#         'type_objet': type_objet,
#         'objet_id': objet_id,
#         'titre_initial': titre_initial,
#         'objet': objet 
#     })



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