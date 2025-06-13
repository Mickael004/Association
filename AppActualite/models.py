from django.db import models
from AppMembre.models import *
# Create your models here.
class Actualite (models.Model):
    membre = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    titre = models.CharField(max_length=50)
    contenue = models.TextField()
    image = models.ImageField(upload_to='static/images')
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        self.titre


class Commentaire(models.Model):
    actualite = models.ForeignKey(Actualite,on_delete=models.CASCADE)
    mombre = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    contenue = models.TextField()
    date_com = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        self.contenue