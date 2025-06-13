from django.db import models

# Create your models here.
class Role(models.Model):
    tire = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        self.titre

class Utilisateur(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=50)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='static/images')
    email = models.EmailField()
    mot_de_passe = models.TextField()
    date_inscription = models.DateField(auto_now_add=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)

    def __str__(self):
        self.titre