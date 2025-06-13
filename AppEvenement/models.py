from django.db import models

# Create your models here.
class Evenement(models.Model):
    ROLE_CHOICES = (
        ('en_cour','En cour'),
        ('terminer','Terminer'),
        ('annuler','Annuler')

    )
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.TextField()
    nombre_max = models.IntegerField()
    statu = models.CharField(max_length=10,choices=ROLE_CHOICES,default='en_cour')
    image = models.ImageField(upload_to='static/images',blank=True,null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        self.nom