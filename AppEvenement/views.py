from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils import timezone

# Create your views here.


def listEvenement(request):
    date_aujour = timezone.now()
    evenement_tous = Evenement.objects.order_by('-date_creation')
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

