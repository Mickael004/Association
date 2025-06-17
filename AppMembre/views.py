from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import *
# from .form import *
import re #regex
from datetime import datetime
import hashlib
from django.contrib.auth import logout
# Create your views here.

def mdp_crypter(mot_de_passe):
    #Hachage 
    mdp = hashlib.sha384()
    mdp.update(mot_de_passe.encode('utf-8'))
    return mdp.hexdigest()

def inserer_photo(request,nom):
    if request.FILES.get("photo"):
        image = request.FILES.get("photo")
        #Enregistrement avec nom unique
        with open(f"static/images/membres/{nom}.jpg","wb") as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        return f"{nom}.jpg"
    
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
        photo = request.FILES.get("photo")
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
                        
                        inscrire = Utilisateur(
                            nom=nom,
                            prenom = prenom,
                            date_naissance = date_naissance,
                            telephone = telephone,
                            adresse = adresse,
                            photo = f"static/images/membres/{inserer_photo(request,dernier)}" ,
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
                            "role" : inscrire.role
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
                    "role":emailExist.role
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


# def editProfil(request):
#     membre = request.session.get('membres',{})
#     utilisateur = get_object_or_404(Utilisateur,id = membre.get('id'))
#     if request.method =='POST':
#         form = ProfilForm(request.POST,request.FILES,instance=utilisateur)
#         if form.is_valid():
#             update_utilisateur = form.save()
#             request.session['membres'] = {
#                 **membre,
#                 "nom":update_utilisateur.nom,
#                 "prenom":update_utilisateur.prenom,
#                 "date_naissance": str(update_utilisateur.date_naissance) if update_utilisateur.date_naissance else "",
#                 "telephone": update_utilisateur.telephone or "",
#                 "email": update_utilisateur.email,
#                 "photo": str(update_utilisateur.photo) if update_utilisateur.photo else "",
#                 "role" : update_utilisateur.role

#             }
            
#             return redirect('profil')
#         else:
#             form = ProfilForm(instance=utilisateur)
    
#     return render(request, 'edit_profil.html', {
#         'form': form,
    #     'membre': membre
    # })

