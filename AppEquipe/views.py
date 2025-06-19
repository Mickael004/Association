from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from AppMembre.models import Utilisateur
from .models import Equipe

# Create your views here.

def liste_membres(request):
    membres = Utilisateur.objects.all()
    equipe_membres_ids = Equipe.objects.values_list('membre_id', flat=True)
    
    membres_avec_statut = []
    for membre in membres:
        dans_equipe = membre.id in equipe_membres_ids
        membres_avec_statut.append({
            'membre': membre,
            'dans_equipe': dans_equipe,
            'role_equipe': Equipe.objects.filter(membre=membre).first().role if dans_equipe else None
        })
    
    return render(request, 'MembreListe.html', {
        'membres_avec_statut': membres_avec_statut
    })



def ajouter_equipe(request, membre_id):
    membre = get_object_or_404(Utilisateur, id=membre_id)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        ordre_affichage = request.POST.get('ordre_affichage', 0)
        
        # Créer ou mettre à jour l'entrée dans l'équipe
        Equipe.objects.update_or_create(
            membre=membre,
            defaults={
                'role': role,
                'ordre_affichage': ordre_affichage
            }
        )
        messages.success(request, f"{membre.prenom} {membre.nom} a été ajouté à l'équipe")
        return redirect('liste_membres')
    
    # Si GET, on affiche juste la modal via le template
    return redirect('liste_membres')

def retirer_equipe(request, membre_id):
    membre = get_object_or_404(Utilisateur, id=membre_id)
    Equipe.objects.filter(membre=membre).delete()
    messages.success(request, f"{membre.prenom} {membre.nom} a été retiré de l'équipe")
    return redirect('liste_membres')