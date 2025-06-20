from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import ArticleBlog,CommentaireBlog
from django.utils import timezone,timesince
from AppMembre.models import Utilisateur

import os
from django.conf import settings
from django.core.files.storage import default_storage

# Create your views here.
def listeArticle(request):
    
    articles = ArticleBlog.objects.filter(publie=True).order_by('-date_publication')
    return render(request,'Blog.html',{'articles':articles})

def detail_article(request,form_id):
    article = get_object_or_404(ArticleBlog, id=form_id,publie=True)
    commentaires = CommentaireBlog.objects.filter(article=article).order_by('date_commentaire')

    if request.method == 'POST' and 'commentaire' in request.POST:
        auteur = Utilisateur.objects.get(id= request.session['membres']['id'])
        if request.session.get('membres'):
            CommentaireBlog.objects.create(
                article = article,
                auteur = auteur,
                message = request.POST['commentaire']
            )
            messages.success(request,'Votre Commmentaire est ajouté')
            messages.success(request, "Votre commentaire a été ajouté !")
            return redirect('detail_article',form_id=form_id)
        else:
            messages.error(request, "Vous devez être connecté pour commenter")
            return redirect('connexion')
    return render(request, 'BlogDetail.html', {
        'article': article,
        'commentaires': commentaires,
        'membre': request.session.get('membres')
    })


def inserer_photo(request, titre):
    if 'image' in request.FILES:
        image = request.FILES['image']
        nom_fichier = f"{titre.replace(' ', '_')}_{image.name}"
        chemin_relatif = os.path.join('images/Blogs', nom_fichier)
        
        
        chemin_absolu = os.path.join(settings.MEDIA_ROOT, 'images/blogs', nom_fichier)
        
        
        os.makedirs(os.path.dirname(chemin_absolu), exist_ok=True)
        
        
        with default_storage.open(chemin_absolu, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        return chemin_relatif 
    

def creer_article(request):
    # Vérification des permissions
    if not request.session.get('membres', {}).get('role') in ['admin', 'moderateur']:
        messages.error(request, "Accès réservé aux administrateurs")
        return redirect('accueil')
    
    
    titre = request.POST.get('titre')
    contenu = request.POST.get('contenue')
    publie = request.POST.get('publie') == 'on'
    date = timezone.now().date()
    nom_image = f"{titre}_{date}"
    if request.method == 'POST':
        try:
            auteur = Utilisateur.objects.get(id= request.session['membres']['id'])
            if not titre or not contenu:
                messages.error(request, "Le titre et le contenu sont obligatoires")
                return render(request, 'ArticleCreer.html', {
                    'titre': titre,
                    'contenue': contenu,
                    'publie': publie,
                    'membre': request.session.get('membres')
                })

            

            # Gestion de l'image
            if 'image' in request.FILES:

                chemin_image = inserer_photo(request,nom_image)
                article = ArticleBlog(
                    titre=titre,
                    contenue=contenu,
                    image=chemin_image,
                    auteur=auteur,
                    publie=publie
                )

                article.save()
                messages.success(request, "Article créé avec succès !")
                return redirect('listeArticle')

        except Exception as e:
            messages.error(request, f"Une erreur est survenue: {str(e)}")
            return render(request, 'ArticleCreer.html', {
                'titre': titre,
                'contenue': contenu,
                'publie': publie,
                'membre': request.session.get('membres')
            })

    # GET request - afficher le formulaire vide
    return render(request, 'ArticleCreer.html', {
        'membre': request.session.get('membres')
    })
