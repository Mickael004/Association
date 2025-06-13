from django.db import models

# Create your models here.

class Activite(models.Model):
    titre = models.CharField(max_length=100)
    descriptiom = models.TextField()
    date = models.DateField()
    horaire = models.TimeField()
    lieu = models.TextField()
    image = models.ImageField(upload_to='static/images',blank=True,null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        self.titre