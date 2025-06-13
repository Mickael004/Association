from django.db import models

# Create your models here.
class Role(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        return self.titre

class Utilisateur(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=50)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='static/images/membres/')
    email = models.EmailField()
    mot_de_passe = models.TextField()
    date_inscription = models.DateField(auto_now_add=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD =['username']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    def __str__(self):
        return f"{self.nom}{self.prenom}"
    


class  Cotisation(models.Model):

    STATUT_CHOICES = [
        ('paye','Payé'),
        ('non_paye','Non payé')
    ]

    utilisateur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10,decimal_places=2)
    periode = models.CharField(max_length=50)
    date_limite_paiement = models.DateField()
    date_paiement = models.DateField(auto_now_add=True)
    reference_paiement = models.CharField(max_length=100,blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='non_paye')

    class Meta:
        verbose_name = "Cotisation"
        verbose_name_plural = "Cotisations"
        ordering = ['-periode','utilisateur']

    
    def __str__(self) :
        return f"Cotisation {self.periode} - {self.utilisateur} ({self.get_statut_display()})"