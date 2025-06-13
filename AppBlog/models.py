from django.db import models
from AppMembre.models import Utilisateur

# Create your models here.

class ArticleBlog(models.Model):
    auteur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    contenue = models.TextField()
    image = models.ImageField(upload_to="static/images/blog/")
    date_publication = models.DateTimeField(auto_now_add=True)
    publie = models.BooleanField(default=False,verbose_name="publié")

    class Meta:
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre
    

class CommentaireBlog(models.Model):
    article = models.ForeignKey(ArticleBlog,on_delete=models.CASCADE)
    auteur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    message = models.TextField()
    date_commentaire = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire sur article"
        verbose_name_plural = "Commentaires sur articles"
        ordering = ['date_commentaire']
    
    def __str__(self):
        return f"Commentaire de {self.auteur} sur {self.article}"
