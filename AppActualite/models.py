from django.db import models
from AppMembre.models import Utilisateur
from AppEvenements.models import Activite,Evenement
# Create your models here.
class Actualite (models.Model):
    ETAT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('en_attente', 'En attente de validation'),
        ('publie', 'Publié'),
        ('rejete', 'Rejeté'),
    ]
    auteur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    titre = models.CharField(max_length=50)
    contenue = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='brouillon')
    evenement = models.ForeignKey(Evenement, on_delete=models.SET_NULL, null=True, blank=True)
    activite = models.ForeignKey(Activite, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre
    

class ImageActualite(models.Model):
    actualite = models.ForeignKey(Actualite, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images/actualites/')
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "imageActualite"
        verbose_name_plural = "imageActualite"
        ordering = ['ordre']

    def __str__(self):
        return f"Image pour {self.actualite.titre}"


class Commentaire(models.Model):
    actualite = models.ForeignKey(Actualite,on_delete=models.CASCADE)
    auteur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    message = models.TextField()
    date_commentaire = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['date_commentaire']

    def __str__(self):
        return f"Commentaire de {self.auteur} sur {self.actualite}"
    


