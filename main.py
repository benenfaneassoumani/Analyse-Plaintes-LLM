import pandas as pd
from groq import Groq
import json
import time
import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

# PHASE 1 : Préparation des données

df = pd.read_csv('Comcast.csv')
df_propre = df[['Ticket #', 'Customer Complaint']].copy()

# On prend maintenant les 100 premières lignes
echantillon = df_propre.head(100)

# PHASE 2 : Connexion à l'IA


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyser_plainte(texte_brut):
    consigne = f"""
    Analyse cette plainte client et réponds UNIQUEMENT au format JSON EXACT avec ces 3 clés :
    {{
        "niveau_urgence": "Normal | Élevé | Critique",
        "categorie": "Internet | Facturation | Service Client | Matériel",
        "resume_fr": "Résumé court"
    }}

    IMPORTANT :
    - Ne change PAS les noms des clés
    - Respecte exactement les noms

    Plainte à analyser : "{texte_brut}"
    """

    reponse = client.chat.completions.create(
        messages=[{"role": "user", "content": consigne}],
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"}
    )

    resultat = json.loads(reponse.choices[0].message.content)

    resultat_corrige = {
        "niveau_urgence": resultat.get("niveau_urgence", "Non spécifié"),
        "categorie": resultat.get("categorie", "Non spécifié"),
        "resume_fr": resultat.get("resume_fr", "Résumé non généré")
    }

    return resultat_corrige

# PHASE 3 : Automatisation

panier_resultats = []

for _, ligne in echantillon.iterrows():
    numero_ticket = ligne['Ticket #']
    texte_plainte = ligne['Customer Complaint']

    print(f"Traitement du ticket {numero_ticket}...")

    try:
        resultat_ia = analyser_plainte(texte_plainte)
        resultat_ia['Ticket #'] = numero_ticket
        panier_resultats.append(resultat_ia)

    except Exception as e:
        print(f"Erreur sur le ticket {numero_ticket}: {e}")

    time.sleep(1)

# PHASE 4 : Structuration

df_resultats = pd.DataFrame(panier_resultats)

colonnes_finales = ['Ticket #', 'niveau_urgence', 'categorie', 'resume_fr']
df_resultats = df_resultats[colonnes_finales]

df_final = pd.merge(echantillon, df_resultats, on='Ticket #')

# PHASE 5 : Export

df_final.to_csv('plaintes_clients.csv', index=False, encoding='utf-8-sig')

print("\nAnalyse terminée !")