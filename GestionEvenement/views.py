from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.shortcuts import redirect, render


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Enregistre l'utilisateur
            login(request, user)  # Connecte l'utilisateur
            return redirect('index')  # Redirection après inscription réussie, modifie 'home' en fonction de ta route
        else:
            # Formulaire non valide, les erreurs seront affichées dans le template
            return render(request, "registration/register.html", {"form": form})
    else:
        form = RegistrationForm()  # Crée un formulaire vide pour un accès GET

    return render(request, "registration/register.html", {"form": form})


def index(request):
    return render(request, "index.html")

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
