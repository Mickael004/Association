from django.db import models
from AppMembre.models import Utilisateur
# Create your models here.
class Actualite (models.Model):
    auteur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    titre = models.CharField(max_length=50)
    contenue = models.TextField()
    image = models.ImageField(upload_to='static/images/actualites')
    date_publication = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre


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
    


class Temoignage(models.Model):
    auteur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    contenue = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Temoignage de {self.auteur}"
    


class Equipe(models.Model):
    membre = models.OneToOneField(Utilisateur,on_delete=models.CASCADE)
    role = models.CharField(max_length=100, verbose_name="Rôle dans l'équipe")
    ordre_affichage = models.PositiveIntegerField(default=0)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Équipe"
        ordering = ['ordre_affichage']

    def __str__(self):
        return f"{self.membre} - {self.role}"