import streamlit as st
import pandas as pd


# 1. Configuration générale de la page


st.set_page_config(page_title="Dashboard Comcast", layout="wide")

st.title("📊 Tableau de Bord - Triage des Plaintes Comcast")
st.write("Analyse automatique des 150 premiers tickets pour aider le service client à prioriser les demandes.")


# 2. Lecture du fichier de résultats


try:
    # Lecture du fichier généré par le script principal
    df = pd.read_csv("plaintes_clients.csv")

    # 3. Vérification des colonnes attendues
    

    colonnes_voulues = [
        "Ticket #",
        "Customer Complaint",
        "niveau_urgence",
        "categorie",
        "resume_fr"
    ]

    colonnes_manquantes = [col for col in colonnes_voulues if col not in df.columns]

    if colonnes_manquantes:
        st.error(f"Colonnes manquantes dans le fichier : {colonnes_manquantes}")
    else:
        # On garde uniquement les colonnes utiles pour le dashboard
        df_propre = df[colonnes_voulues].copy()

        
        # 4. Affichage du tableau
       

        st.subheader(f"1. Liste des {len(df_propre)} plaintes analysées")
        st.dataframe(df_propre, use_container_width=True, height=500)

        st.markdown("---")

        
        # 5. Statistiques générales
       

        st.subheader("2. Statistiques et priorisation")

        # Petits indicateurs en haut
        nb_total = len(df_propre)
        nb_critiques = (df_propre["niveau_urgence"] == "Critique").sum()
        nb_categories = df_propre["categorie"].nunique()

        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

        with col_kpi1:
            st.metric("Nombre total de plaintes", nb_total)

        with col_kpi2:
            st.metric("Plaintes critiques", nb_critiques)

        with col_kpi3:
            st.metric("Nombre de catégories", nb_categories)

        st.markdown("---")

        
        # 6. Graphiques
        

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Répartition par catégorie**")
            stats_cat = df_propre["categorie"].value_counts()
            st.bar_chart(stats_cat)

        with col2:
            st.write("**Répartition par niveau d'urgence**")
            stats_urgence = df_propre["niveau_urgence"].value_counts()
            st.bar_chart(stats_urgence)

        st.markdown("---")

        
        # 7. Filtrage simple
        

        st.subheader("3. Filtrer les plaintes")

        categories_disponibles = ["Toutes"] + sorted(df_propre["categorie"].dropna().unique().tolist())
        urgences_disponibles = ["Toutes"] + sorted(df_propre["niveau_urgence"].dropna().unique().tolist())

        filtre_cat = st.selectbox("Choisir une catégorie", categories_disponibles)
        filtre_urgence = st.selectbox("Choisir un niveau d'urgence", urgences_disponibles)

        df_filtre = df_propre.copy()

        if filtre_cat != "Toutes":
            df_filtre = df_filtre[df_filtre["categorie"] == filtre_cat]

        if filtre_urgence != "Toutes":
            df_filtre = df_filtre[df_filtre["niveau_urgence"] == filtre_urgence]

        st.write(f"Nombre de plaintes après filtrage : **{len(df_filtre)}**")
        st.dataframe(df_filtre, use_container_width=True, height=400)

except FileNotFoundError:
    st.error("⚠️ Le fichier 'plaintes_clients.csv' est introuvable. Lance d'abord le script principal qui génère ce fichier.")

except Exception as e:
    st.error(f"Une erreur est survenue : {e}")