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
    adresse = models.CharField(max_length=50,blank=True, null=True)
    photo = models.ImageField(upload_to='static/images/membres/')
    email = models.EmailField()
    mot_de_passe = models.TextField()
    date_inscription = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=50)
    # role = models.ForeignKey(Role,on_delete=models.CASCADE)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD =['username']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    def __str__(self):
        return f"{self.nom}{self.prenom}"
    

class Cotisation(models.Model):
    TYPE_CHOICES = [
        ('annuelle', 'Annuelle'),
        ('mensuelle', 'Mensuelle'),
        ('ponctuelle', 'Ponctuelle'),
    ]

    STATUT_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    titre = models.CharField(max_length=100)
    description = models.TextField()
    montant = models.IntegerField()
    type_cotisation = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.titre} - {self.montant}Ar"
    

class Paiement(models.Model):
    METHOD_CHOICS =[
        ('espece', 'Espèces'),
        ('cheque', 'Chèque'),
        ('mobile', 'Mobile Money'),
        ('carte', 'Carte bancaire'),
    ]

    STATUT_CHOICES =[
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]

    membre = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    cotisation = models.ForeignKey(Cotisation, on_delete=models.CASCADE)
    date_paiement = models.DateField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode_paiement = models.CharField(max_length=50, choices=METHOD_CHOICS)
    numero_compte=models.CharField(max_length=15)
    preuve_paiement = models.FileField(upload_to='static/paiements/preuves/', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    notes = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ['-date_paiement']

    def __str__(self):
        return f"{self.membre} - {self.cotisation} - {self.date_paiement}"


# class Cotisation(models.Model):

#     STATUT_CHOICES = [
#         ('paye','Payé'),
#         ('non_paye','Non payé')
#     ]

#     utilisateur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
#     montant = models.DecimalField(max_digits=10,decimal_places=2)
#     periode = models.CharField(max_length=50)
#     date_limite_paiement = models.DateField()
#     date_paiement = models.DateField(auto_now_add=True)
#     reference_paiement = models.CharField(max_length=100,blank=True, null=True)
#     statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='non_paye')

#     class Meta:
#         verbose_name = "Cotisation"
#         verbose_name_plural = "Cotisations"
#         ordering = ['-periode','utilisateur']

    
#     def __str__(self) :
#         return f"Cotisation {self.periode} - {self.utilisateur} ({self.get_statut_display()})"