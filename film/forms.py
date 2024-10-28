from django import forms
from .models import Film,Personnage,Projet,EffetSonoreVisuelles

class SentimentAnalysisForm(forms.Form):
    scenario_text = forms.CharField(widget=forms.Textarea, label='Scenario Text')
class EffetSonoreVisuellesForm(forms.ModelForm):
    class Meta:
        model = EffetSonoreVisuelles
        fields = ['titre', 'description','projet', 'typeEffet']

    def clean_titre(self):
        titre = self.cleaned_data.get('titre')
        if len(titre) < 3:
            raise forms.ValidationError("Le titre doit contenir au moins 3 caractères.")
        return titre

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 3:
            raise forms.ValidationError("La description doit contenir au moins 3 caractères.")
        return description

class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ['title', 'genre']  # Make sure to include all necessary fields

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError("Le titre doit contenir au moins 3 caractères.")
        return title

    def clean_genre(self):
        genre = self.cleaned_data.get('genre')
        if len(genre) < 3:
            raise forms.ValidationError("Le genre doit contenir au moins 3 caractères.")
        return genre
class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['titre', 'realisateur', 'annee_sortie', 'genre']
class PersonnageForm(forms.ModelForm):
    class Meta:
        model = Personnage
        fields = ['nom', 'description']

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) < 3:
            raise forms.ValidationError("Le nom doit contenir au moins 3 caractères.")
        return nom

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 3:
            raise forms.ValidationError("La description doit contenir au moins 3 caractères.")
        return description
