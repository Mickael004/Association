from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from .models import *
# from .form import *
import re #regex
from datetime import datetime
import hashlib
from django.contrib.auth import logout
import os
from django.conf import settings
from django.core.files.storage import default_storage
# Create your views here.

def mdp_crypter(mot_de_passe):
    #Hachage 
    mdp = hashlib.sha384()
    mdp.update(mot_de_passe.encode('utf-8'))
    return mdp.hexdigest()

def inserer_photo(request, nom):
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        nom_fichier = f"{nom.replace(' ', '_')}_{photo.name}"
        chemin_relatif = os.path.join('images/utilisateurs', nom_fichier)
        
        
        chemin_absolu = os.path.join(settings.MEDIA_ROOT, 'images/utilisateurs', nom_fichier)
        
        
        os.makedirs(os.path.dirname(chemin_absolu), exist_ok=True)
        
        
        with default_storage.open(chemin_absolu, 'wb+') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)
        
        return chemin_relatif
    
def inscriptionPage(request):
    if request.session.get('membres'):
        return redirect('accueil')
    else:
        return render(request,'inscription.html')
def inscrire_membre(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get("prenom")
        date_naissance = request.POST.get('date_naissance')
        telephone = request.POST.get("telephone")
        adresse = request.POST.get("adresse")
        emails = request.POST.get("email")
        mot_de_passe = request.POST.get("mot_de_passe")
        role = request.POST.get("role")
        confirm_pwd = request.POST.get("confirm_pwd")

        if nom and prenom and emails:
            if not Utilisateur.objects.filter(email=emails).exists():
                if mot_de_passe==confirm_pwd:
                    if len(mot_de_passe)>= 8 and re.search(r'[A-Za-z]',mot_de_passe) and re.search(r'[0-9]',mot_de_passe):
                            
                        aff = prenom
                        long_nom = len(nom)
                        dernier = f"{aff[:3]}_{long_nom}"
                        if 'photo' in request.FILES:
                            chemin_image = inserer_photo(request,dernier)
                            inscrire = Utilisateur(
                                nom=nom,
                                prenom = prenom,
                                date_naissance = date_naissance,
                                telephone = telephone,
                                adresse = adresse,
                                photo = chemin_image ,
                                email = emails,
                                date_inscription = datetime.now(),
                                mot_de_passe = mdp_crypter(mot_de_passe),
                                role = role
                                
                            )
                            inscrire.save()
                            #creation session

                            request.session['membres'] = {
                                "id" : inscrire.id,
                                "nom" : inscrire.nom,
                                "prenom" : inscrire.prenom,
                                "date_naissance" : inscrire.date_naissance,
                                "telephone":inscrire.telephone,
                                "adresse":inscrire.adresse,
                                "email" : inscrire.email,
                                "photo" : str(inscrire.photo),
                                "role" : inscrire.role,
                                "mot_de_passe": inscrire.mot_de_passe
                                }
                            return redirect('http://127.0.0.1:8000/')
                    else:
                       return render(request,'inscription.html',{'error':"Mots de passe doit inclure au moins 8 caractères et inclue les lettre et les  chiffre"}) 
                else:
                    return render(request,'inscription.html',{'error':"Mots de passe ne correspond pas"})
            else :
                return render(request,'inscription.html',{'error':"Email Deja une compte"})


        else:
            return render(request,'inscription.html',{'error':"Tous les champs sont obligatoire"})
        
# connexion
def connexionPage(request):
    return render(request,'login.html')
    # if request.session.get('membres'):
    #     return redirect('accueil')
    # else:
    #     return render('login.html')
def connexion(request):
    if request.method == 'POST':
        # emails = str(request.POST.get('email',''))
        emails = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')

        if emails == "" or mot_de_passe == "":
            return render(request,'login.html', {'error':"Tous les champs sont Obligatoires"})
        
        try:
            emailExist = Utilisateur.objects.get(email = emails)

            if mdp_crypter(mot_de_passe) == emailExist.mot_de_passe:
                membreConnect = {
                    "id" : emailExist.id,
                    "nom" : emailExist.nom,
                    "prenom" : emailExist.prenom,
                    "date_naissance": str(emailExist.date_naissance),
                    "telephone":emailExist.telephone,
                    "adresse":emailExist.adresse,
                    "email" : emailExist.email,
                    "photo" : str(emailExist.photo),
                    "role":emailExist.role,
                    "mot_de_passe" : emailExist.mot_de_passe
                }
                request.session['membres'] = membreConnect
                return redirect('accueil')
            else:
               return render(request,'login.html',{'error': "Vérifier votre Mots de passe !"}) 
            
        except Utilisateur.DoesNotExist:
            return render(request,'login.html',{'error': "Vous n'êtes pas inscrit !"})
        

def deconnexion(request):
    logout(request)
    request.session.clear()
    return redirect('connexionPage')

# Profil
def profil(request):
    if request.session.get('membres'):
        membre_session = request.session['membres']
        cotisation = Cotisation.objects.filter(utilisateur_id = membre_session.get('id')).order_by('-periode')

        print ('Session: ',membre_session)
        return render(request,'Profil.html',{
            'membre':membre_session,
            'cotisation':cotisation,
            'MEDIA_URL':settings.MEDIA_URL
        })
    else:
        return redirect('accueil')

def updateProfile(request):
    if request.session.get('membres') and request.method == 'POST':
        try:
            membres =Utilisateur.objects.get(id=request.session['membres']['id'])

            membres.nom = request.POST.get('nom')
            membres.prenom = request.POST.get('prenom')
            membres.email = request.POST.get('email')
            membres.adresse = request.POST.get('adresse')
            membres.telephone = request.POST.get('telephone')
            membres.date_naissance = request.POST.get('date_naissance')

            if 'photo' in request.FILES:
                aff = membres.prenom
                long_nom = len(membres['nom'])
                dernier = f"{aff[:3]}_{long_nom}"
                filename = f"images/membres/{inserer_photo(request,dernier)}" 
                membres.photo = filename

            membres.save()
            # mise jour session
            request.session['membres'] = {
                'id':membres.id,
                'nom':membres.nom,
                'prenom':membres.prenom,
                "date_naissance": str(membres.date_naissance),
                "telephone":membres.telephone,
                "adresse":membres.adresse,
                "email" : membres.email,
                "photo" : str(membres.photo),
                "role":membres.role,
                "mot_de_passe" : membres.mot_de_passe
            }
            request.session.modified = True

            messages.success(request,'Profil Mis à jour avec success')

        except Exception as e :
            messages.error(request,f'Erreur lors de mise à jour')

        return redirect('profil')
    
    return redirect('profil')


def modif_mot_passe(request):
    if request.method == 'POST' and request.session.get('membres'):
        
        ancien_motPasse = request.POST.get("ancien_password")
        nouveau_motPasse = request.POST.get("nouveau_password")
        confirm_motPasse = request.POST.get("confirm_password")

        try:
            membres = Utilisateur.objects.get(id=request.session['membres']['id'])

            if not mdp_crypter(ancien_motPasse) == membres.mot_de_passe:
                messages.error(request,"Mots de passe actuel incorrecte")
                return redirect('profil')
                
        
            if nouveau_motPasse != confirm_motPasse:
                messages.error(request,"Les nouveaux mots de passe ne correspond pas")
                return redirect('profil')
        
            # Mise a jour
            membres.mot_de_passe = mdp_crypter(nouveau_motPasse)
            membres.save()

            messages.success(request,"Mots de passe à jour avec succés")

        except Exception as e :
            messages.error(request,f'Erreur  lors de mise à jour')

        return redirect('profil')
    return redirect('profil')
            




# //////////////Cotisation

def ajouter_cotisation(request):
    if request.session.get('membres', {}).get('role')  in ['admin', 'moderateur']:
        if request.method == 'POST':
            try:
                utilisateur = Utilisateur.objects.get(id=request.session['membres']['id'])

                montant = request.POST.get('montant')
                periode = request.POST.get('periode')
                date_limite = request.POST.get('date_limite')
                
                cotisation = Cotisation(
                    utilisateur=utilisateur,
                    montant=montant,
                    periode=periode,
                    date_limite_paiement=date_limite,
                    statut='non_paye'
                )
                cotisation.save()
                
                messages.success(request, "Cotisation ajoutée avec succès!")
                return redirect('liste_cotisations')
            
            except Exception as e:
                messages.error(request, f"Erreur: {str(e)}")
        # Liste des membres pour le select
    membres = Utilisateur.objects.all().order_by('nom', 'prenom')
    return render(request, 'cotisation/Ajouter.html', {'membres': membres})


def liste_cotisations(request):
    cotisations = Cotisation.objects.all().select_related('utilisateur').order_by('-periode')
    # Filtres
    membre_id = request.GET.get('membre')
    statut = request.GET.get('statut')
    
    if membre_id:
        cotisations = cotisations.filter(utilisateur_id=membre_id)
    if statut:
        cotisations = cotisations.filter(statut=statut)
    
    context = {
        'cotisations': cotisations,
        'membres': Utilisateur.objects.all().order_by('nom'),
    }
    return render(request, 'cotisation/Liste.html', context)
