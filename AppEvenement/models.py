from django.db import models
from AppMembre.models import Utilisateur

# Create your models here.
    # ROLE_CHOICES = (
    #     ('prochainement','Prochainement'),
    #     ('en_cours','En cours'),
    #     ('termine','Terminé'),
    #     ('annule','Annulé')

    # )
class Evenement(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    nombre_participant_max = models.PositiveIntegerField(blank=True,null=True)
    image = models.ImageField(upload_to='static/images/evenements',blank=True,null=True)

    createur = models.ForeignKey(Utilisateur,on_delete=models.SET_NULL, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField(Utilisateur, related_name="evenement_participes", blank=True)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-date_debut']


    def __str__(self) :
        return self.titre
    

class ParticipationEvenement(models.Model):
    evenement = models.ForeignKey(Evenement,on_delete=models.CASCADE)
    participant = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    date_inscription= models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Participation à un événement"
        verbose_name_plural = "Participations aux événements"
        unique_together = ('evenement', 'participant')

    def __str__(self):
        return f"{self.participant} à {self.evenement}"
    



class Activite(models.Model):
    ROLE_CHOICES = (
        ('en_attent','En attente'),
        ('en_cours','En cours'),
        ('termine','Terminé'),
        ('annule','Annulé')

    )
    nom = models.CharField(max_length=200)
    description = models.TextField()
    date_organisation = models.DateField()
    horaire_debut = models.TimeField()
    horaire_fin = models.TimeField( blank=True, null=True)
    lieu = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/images/activites/', verbose_name="Image", blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    createur = models.ForeignKey(Utilisateur,on_delete=models.SET_NULL, null=True, verbose_name="Créateur")
    
    participants = models.ManyToManyField(Utilisateur, related_name='activites_participes', blank=True)
    
    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['-date_organisation']
    
    def __str__(self):
        return self.nom
    
    

class ParticipationActivite(models.Model):
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    participant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Participation à une activité"
        verbose_name_plural = "Participations aux activités"
        unique_together = ('activite', 'participant')
    
    def __str__(self):
        return f"{self.participant} à {self.activite}"
