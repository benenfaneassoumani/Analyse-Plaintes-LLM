#  Assistant IA pour le Service Client

**Analyse sémantique et priorisation automatique des plaintes clients à l’aide d’un modèle de langage (LLM).**

---

##  Présentation

Ce projet automatise l’analyse de plaintes clients en utilisant une IA.
À partir de données brutes (tickets clients), le pipeline extrait des informations clés permettant d'accélérer la prise en charge, d'améliorer la satisfaction client et de guider les décisions opérationnelles.

 **Application en ligne** :
https://analyse-plaintes-llm-h7dbtqdaez8nqrhedw7bbm.streamlit.app/


---

##  Objectifs Métier

* Prioriser les urgences (Normal / Élevé / Critique)
* Identifier les types de problèmes (Internet, Facturation, Matériel)
* Accélérer le traitement des tickets grâce à des résumés automatiques

---

##  Fonctionnement du Pipeline

1. Chargement des données (CSV)
2. Analyse sémantique via un LLM (Llama 3)
3. Extraction structurée (JSON)
4. Visualisation via un dashboard interactif

---

##  Stack Technique

* Python / Pandas
* Groq API (Llama 3.1 8b)
* Streamlit
* Dotenv (sécurité des clés API)

---

## 📊 Fonctionnalités du Dashboard

* Affichage des tickets analysés
* Répartition par catégorie
* Analyse du niveau d’urgence
* KPI (nombre total, cas critiques)
* Filtres interactifs

---

##  Lancer le projet en local

### 1. Cloner le projet

git clone https://github.com/benenfaneassoumani/Analyse-Plaintes-LLM.git


cd Analyse-Plaintes-LLM

### 2. Installer les dépendances

pip install -r requirements.txt

### 3. Configurer la clé API

Créer un fichier `.env` à la racine :

GROQ_API_KEY=votre_cle_api_ici

### 4. Lancer le projet

python main.py
streamlit run dashboard.py

---

##  Auteur

Projet réalisé par **Ben-enfane Assoumani**
Étudiant  en Master Statistique et Sciences des données

Montpellier
