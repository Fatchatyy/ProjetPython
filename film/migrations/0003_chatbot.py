# Generated by Django 4.1 on 2024-10-10 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('film', '0002_scenario'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_input', models.CharField(max_length=500)),
                ('gemini_output', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GeminiUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
