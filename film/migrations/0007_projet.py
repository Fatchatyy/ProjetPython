# Generated by Django 4.1 on 2024-10-27 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0006_alter_personnage_description_alter_personnage_nom_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projet',
            fields=[
                ('idProjet', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=100)),
            ],
        ),
    ]
