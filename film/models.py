from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Projet(models.Model):
    idProjet = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Adjust 'projet_detail' to the actual name of your project detail view
        return reverse('module:projet_detail', kwargs={'pk': self.pk})
class Personnage(models.Model):
    nom = models.CharField(
        max_length=100, 
        validators=[MinLengthValidator(3)],  # Longueur minimale de 3 caractères
        verbose_name="Nom du personnage"
    )
    description = models.TextField(
        blank=False,  # Rend le champ obligatoire
        validators=[MinLengthValidator(3)],  # Longueur minimale de 3 caractères
        verbose_name="Description"
    )

    likes = models.ManyToManyField(User, related_name='liked_personnages', blank=True)
    date_creation = models.DateField(auto_now_add=True)  # Date de création du personnage
    def get_absolute_url(self):
        # Assure-toi que 'personnage_detail' est le nom de la vue qui affiche le détail d'un personnage
        return reverse('module:personnage_detail', kwargs={'pk': self.pk})
    def total_likes(self):
        return self.likes.count()

    def user_has_liked(self, user):
        return user in self.likes.all()
    def __str__(self):
        return self.nom
    
class EffetSonoreVisuelles(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_creation = models.DateField(auto_now_add=True)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='effets')
    
    TYPE_CHOICES = [
        ('Visual', 'Visual'),
        ('Sound', 'Sound'),
    ]
    typeEffet = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('module:effetsonorevisuelles_detail', kwargs={'pk': self.pk})
class Comment(models.Model):
    personnage = models.ForeignKey(Personnage, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(validators=[MinLengthValidator(3)], verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.personnage.nom}'
class scenario(models.Model):
    titre = models.CharField(max_length=255)  
    description = models.TextField()        

    date_creation = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.titre
    def get_absolute_url(self):
      
        return reverse('module:scenario_detail', kwargs={'pk': self.pk})
class ChatBot(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="GeminiUser", null=True
    )
    text_input = models.CharField(max_length=500)
    gemini_output = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.text_input
class Film(models.Model):
    titre = models.CharField(max_length=200)
    realisateur = models.CharField(max_length=100)
    annee_sortie = models.IntegerField()
    genre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.titre