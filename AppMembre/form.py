from django import forms
from django.core.exceptions import ValidationError
from .models import Utilisateur
from django.core.validators import RegexValidator

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = [
            'nom',
            'prenom',
            'email',
            'date_naissance',
            'telephone',
            'adresse',
            'photo',
            'mot_de_passe',
            'role',
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+261 32 34 564 78'
            }),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de naissance',
            'telephone': 'Téléphone',
            'adresse':'adresse',
            'photo': 'Photo de profil',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajout des classes Bootstrap aux champs non couverts par les widgets
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['class'] = 'form-control'
        
        # Validation personnalisée pour le téléphone
        self.fields['telephone'].validators.append(
            RegexValidator(
                regex=r'^\+?[0-9\s]{10,15}$',
                message="Format de téléphone invalide. Exemple: +33 6 12 34 56 78"
            )
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if Utilisateur.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("Cet email est déjà utilisé par un autre membre")
        return email

    def clean_date_naissance(self):
        date_naissance = self.cleaned_data['date_naissance']
        return date_naissance
