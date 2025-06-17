from django.shortcuts import render

# Create your views here.
def accueilpage(request):
    return render(request,'Accueil.html')