from django.db import models
from AppMembre.models import Utilisateur
# Create your models here.

class MessagePrive(models.Model):
    expediteur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE,related_name="message_envoyes",verbose_name="Expéditeur")
    destinataire = models.ForeignKey(Utilisateur,on_delete=models.CASCADE,related_name="message_recus",verbose_name='Destinataire')
    sujet = models.CharField(max_length=200)
    contenue = models.TextField()
    date_envoie = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message privé"
        verbose_name_plural = "Messages privés"
        ordering = ['-date_envoie']
    def __str__(self):
        return f"{self.sujet} - De {self.expediteur} à {self.destinataire}"



class Notification(models.Model):
    TYPE_NOTIFICATION = [
        ('evenement', 'Événement'),
        ('commentaire', 'Commentaire'),
        ('message', 'Message privé'),
        ('cotisation', 'Cotisation'),

    ]

    utilisateur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    type_notification = models.CharField(max_length=20,choices=TYPE_NOTIFICATION)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    lien = models.URLField(blank=True,null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.titre} - {self.utilisateur}"
