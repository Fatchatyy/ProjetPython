
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Personnage,scenario,ChatBot,Film, Comment,Projet,EffetSonoreVisuelles
from django.urls import reverse_lazy
from .mixins import AdminRequiredMixin  # Import du mixin personnalisé
from django.shortcuts import render, reverse,get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests
from django.conf import settings
from transformers import pipeline

sentiment_analysis = pipeline("sentiment-analysis")

# views.py

from io import BytesIO
from PIL import Image
import base64
import requests 
import io
from .forms import FilmForm, PersonnageForm,ProjetForm,EffetSonoreVisuellesForm,SentimentAnalysisForm

# Create your views here.

class EffetSonoreVisuellesListView(LoginRequiredMixin, ListView):
    model = EffetSonoreVisuelles
    template_name = 'effetsonorevisuelles/effetsonorevisuelles_list.html'

class EffetSonoreVisuellesDetailView(LoginRequiredMixin, DetailView):
    model = EffetSonoreVisuelles
    template_name = 'effetsonorevisuelles/effetsonorevisuelles_detail.html'

class EffetSonoreVisuellesCreateView(LoginRequiredMixin, CreateView):
    model = EffetSonoreVisuelles
    template_name = 'effetsonorevisuelles/effetsonorevisuelles_form.html'
    form_class = EffetSonoreVisuellesForm

class EffetSonoreVisuellesUpdateView(LoginRequiredMixin, UpdateView):
    model = EffetSonoreVisuelles
    template_name = 'effetsonorevisuelles/effetsonorevisuelles_form.html'
    form_class = EffetSonoreVisuellesForm

class EffetSonoreVisuellesDeleteView(LoginRequiredMixin, DeleteView):
    model = EffetSonoreVisuelles
    template_name = 'effetsonorevisuelles/effetsonorevisuelles_confirm_delete.html'
    success_url = reverse_lazy('module:effetsonorevisuelles_list')

# List all projects
class ProjetListView(LoginRequiredMixin, ListView):
    model = Projet
    template_name = 'projet/projet_list.html'  # Template for listing projects

class ProjetDetailView(LoginRequiredMixin, DetailView):
    model = Projet
    template_name = 'projet/projet_detail.html'  # Template for project detail view

class ProjetCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Projet
    template_name = 'projet/projet_form.html'  # Template for project creation
    form_class = ProjetForm  # Form for creating/updating a project

class ProjetUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Projet
    template_name = 'projet/projet_form.html'  # Template for project update
    form_class = ProjetForm  # Form for creating/updating a project


class ProjetDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Projet
    template_name = 'projet/projet_confirm_delete.html'  # Template for confirming project deletion
    success_url = reverse_lazy('module:projet_list')  # Redirect after deletion

# add here to your generated API key

class PersonnageListView(LoginRequiredMixin, ListView):
    model = Personnage
    template_name = 'personnage/personnage_list.html'

class PersonnageDetailView(LoginRequiredMixin,DetailView):
    model = Personnage
    template_name = 'personnage/personnage_detail.html'

class PersonnageCreateView(LoginRequiredMixin,AdminRequiredMixin, CreateView):
    model = Personnage
    template_name = 'personnage/personnage_form.html'
    form_class = PersonnageForm

class PersonnageUpdateView(LoginRequiredMixin,AdminRequiredMixin, UpdateView):
    model = Personnage
    form_class = PersonnageForm
    template_name = 'personnage/personnage_form.html'


class PersonnageDeleteView(LoginRequiredMixin,AdminRequiredMixin, DeleteView):
    model = Personnage
    template_name = 'personnage/personnage_confirm_delete.html'
    success_url = reverse_lazy('module:personnage_list')



class scenarioListView(LoginRequiredMixin, ListView):
    model = scenario
    template_name = 'scenario/scenario.html'

class scenarioDetailView(LoginRequiredMixin, DetailView):
    model = scenario
    template_name = 'scenario/scenario_detail.html'

class scenarioCreateView(LoginRequiredMixin,AdminRequiredMixin, CreateView):
    model = scenario
    template_name = 'scenario/scenario_form.html'
    fields = ['titre', 'description']  # Ajoute tes champs ici

class scenarioUpdateView(LoginRequiredMixin,AdminRequiredMixin, UpdateView):
    model = scenario
    template_name = 'scenario/scenario_form.html'
    fields = ['titre', 'description']

class scenarioDeleteView(LoginRequiredMixin,AdminRequiredMixin, DeleteView):
    model = scenario
    template_name = 'scenario/scenario_confirm_delete.html'
    success_url = reverse_lazy('module:scenario_list')


@login_required
def add_comment(request, personnage_id):
    personnage = get_object_or_404(Personnage, pk=personnage_id)
    content = request.POST.get('content')

    if content:
        Comment.objects.create(personnage=personnage, user=request.user, content=content)

    return redirect(personnage.get_absolute_url())

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    personnage = comment.personnage
    comment.delete()
    return redirect(personnage.get_absolute_url())
@login_required
def ask_question(request):
    if request.method == "POST":
        genai.configure(api_key="AIzaSyCLm9b9MPbGJTUl4DKCWpTxScEon-fpMcs")
        text = request.POST.get("text")
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        response = chat.send_message(text)
        user = request.user
        ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
        # Extract necessary data from response
        response_data = {
            "text": response.text,  # Assuming response.text contains the relevant response data
            # Add other relevant data from response if needed
        }
        return JsonResponse({"data": response_data})
    else:
        return HttpResponseRedirect(
            reverse("chat")
        )  # Redirect to chat page for GET requests

@login_required
def chat(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    return render(request, "chatbot/chat_bot.html", {"chats": chats})
@login_required
def like_personnage(request, pk):
    personnage = get_object_or_404(Personnage, pk=pk)
    if request.user in personnage.likes.all():
        personnage.likes.remove(request.user)
        liked = False
    else:
        personnage.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': personnage.total_likes()})
""" API_URL = "https://api-inference.huggingface.co/models/blink7630/storyboard-sketch"
HEADERS = {"Authorization": "Bearer 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"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise exception if status code isn't 2xx
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error querying API: {e}")  # Log error
        raise

@login_required
@require_POST
def generate_image_ajax(request):
    prompt = request.POST.get('prompt')
    try:
        image_bytes = query({"inputs": prompt})
        image = Image.open(io.BytesIO(image_bytes))

        # Convert the image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return JsonResponse({'image': img_str})

    except Exception as e:
        print(f"Error generating image: {e}")  # Log the error
        return JsonResponse({'error': str(e)}, status=500) 
 """
API_URL = "https://api-inference.huggingface.co/models/Artples/LAI-ImageGeneration-vSDXL-1"
HEADERS = {"Authorization": "Bearer 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"}  # Defined globally

def query(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error querying API: {e}")
        raise

@login_required
@require_POST
def generate_image_ajax(request):
    prompt = request.POST.get('prompt')
    try:
        image_bytes = query({"inputs": prompt})
        image = Image.open(io.BytesIO(image_bytes))

        # Convert the image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return JsonResponse({'image': img_str})
    except Exception as e:
        print(f"Error generating image: {e}")
        return JsonResponse({'error': str(e)}, status=500)
        
@login_required
def film_list(request):
    films = Film.objects.all()
    return render(request, 'film/film_list.html', {'films': films})

@login_required

# Détail d'un film
def film_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    return render(request, 'film/film_detail.html', {'film': film})

@login_required
# Créer un film
def film_create(request):
    if request.method == "POST":
        form = FilmForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module:film_list')
    else:
        form = FilmForm()
    return render(request, 'film/film_form.html', {'form': form})
    
@login_required

# Mettre à jour un film
def film_update(request, pk):
    film = get_object_or_404(Film, pk=pk)
    if request.method == "POST":
        form = FilmForm(request.POST, instance=film)
        if form.is_valid():
            form.save()
            return redirect('module:film_list')
    else:
        form = FilmForm(instance=film)
    return render(request, 'film/film_form.html', {'form': form})

@login_required
# Supprimer un film
def film_delete(request, pk):
    film = get_object_or_404(Film, pk=pk)
    if request.method == "POST":
        film.delete()
        return redirect('module:film_list')
    return render(request, 'film/film_confirm_delete.html', {'film': film})

# Function to call the TextRazor API for sentiment analysis


def analyze_sentiment(text):
    url = "https://api.textrazor.com"
    headers = {
        "X-TextRazor-Key": settings.TESTRAZE_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    print("the text", text)
    payload = {
        "text": text,
        "extractors": ["entailments"]  # Use entailments as the extractor
    }

    response = requests.post(url, data=payload, headers=headers)

    # Log the response for debugging
    if response.status_code == 200:
        sentiment_data = response.json()
        return sentiment_data  # Return the full JSON response for further processing
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Print error message
        return None

@login_required
def sentiment_analysis_view(request):
    sentiment = None
    if request.method == "POST":
        form = SentimentAnalysisForm(request.POST)
        if form.is_valid():
            scenario_text = form.cleaned_data['scenario_text']
            sentiment_data = analyze_sentiment(scenario_text)

            if sentiment_data:
                # Extract entailments from the response
                entailments = sentiment_data['response'].get('entailments', [])
                
                # Log entailments for debugging
                print("EEEntailments:", entailments)

                # Extract and sort relevant words by score
                relevant_words = sorted(entailments, key=lambda x: x['score'], reverse=True)
                top_words = [word['entailedWords'][0] for word in relevant_words[:5]]  # Get top 5 entailed words
                
                # Join the top words into a single string
                input_text_for_emotion = ', '.join(top_words)
                print("!!!??11111!!!the sentiment data in SECOND METHOD IS11111", input_text_for_emotion)

                # Load the emotion classification pipeline
                emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

                # Get emotions
                result = emotion_classifier(input_text_for_emotion)
                print("AAAAAAAAAAAAAAAAAAAA3", result)

                # Log and process the results
                ranked_emotions = sorted(result[0], key=lambda x: x['score'], reverse=True)
                print("AAAAAAAAAAAAAAAAAAAA4", ranked_emotions)
                top_emotions = ranked_emotions[:5]  # Get the top 5 emotions
                print("AAAAAAAAAAAAAAAAAAAA", top_emotions)

                # Prepare the sentiment data for rendering
                sentiment = {emotion['label']: emotion['score'] for emotion in top_emotions}
                print("AAAAAAAAAAAAAAAAAAA5", sentiment)

                # Log the top emotions
                for emotion in top_emotions:
                    print(f"{emotion['label']}: {emotion['score']:.3f}")

            else:
                sentiment = "Error analyzing sentiment."
    else:
        form = SentimentAnalysisForm()

    return render(request, 'sentimentBot/sentiment_analysis.html', {'form': form, 'sentiment': sentiment})