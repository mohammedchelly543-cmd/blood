from django import forms
from django.contrib.auth.models import User
from .models import Donneur, Hopital
from datetime import date

class InscriptionDonneurForm(forms.ModelForm):
    # Champs User
    username = forms.CharField(label='Nom d\'utilisateur', max_length=150)
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Prénom', max_length=100)
    last_name = forms.CharField(label='Nom', max_length=100)
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = Donneur
        fields = ['groupe_sanguin', 'sexe', 'date_naissance', 'ville', 'telephone']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Ce nom d\'utilisateur est déjà pris.')
        return username

    def clean_date_naissance(self):
        date_naissance = self.cleaned_data.get('date_naissance')
        if date_naissance:
            today = date.today()
            age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
            if age < 18:
                raise forms.ValidationError('Vous devez avoir au moins 18 ans pour vous inscrire.')
        return date_naissance


class InscriptionHopitalForm(forms.ModelForm):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = Hopital
        fields = ['nom', 'adresse', 'ville', 'telephone', 'numero_agrement']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Ce nom d\'utilisateur est déjà pris.')
        return username