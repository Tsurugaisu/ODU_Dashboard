import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


col_names = ["date", "chaine", "b", "theme", "nombre_sujets", "duree"]
df = pd.read_csv(
    "Data/ina-barometre-jt-tv-donnees-quotidiennes-2000-2020-nbre-sujets-durees-202410.csv",
    delimiter=";",
    encoding="ISO-8859-1",
    header=None,
    names=col_names,
)
df = df.drop(["b"], axis=1)
df["date"] = pd.to_datetime(df["date"], dayfirst=True)
df["Année"] = df["date"].dt.year

df["duree_minutes"] = df["duree"] / 60
df["duree_heures"] = df["duree"] / 3600


df_st = df[df["theme"] == "Sciences et techniques"]
df_st["Année"] = df_st["date"].dt.year
df_sciences_grouped = df_st.groupby("Année")["duree"].sum() / 3600

# Affichage des graphiques


st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Choisissez un Dashboard :",
    [
        "Présentation du Projet",
        "Analyse Thématique",
        "Sciences",
        "Économie",
        "TF1",
        "Analyse Médias",
        "Comparaison Thèmes",
    ],
)


if page == "Présentation du Projet":
    st.markdown(
        "Bienvenue sur notre projet, réalisé dans le cadre de l'initiative Open Data University, un programme porté par l'association Latitudes pour encourager l'utilisation des données ouvertes au service de la société. \n\n"
        "Notre travail s'inscrit dans le défi *Les Françaises et Français et l audiovisuel*, avec pour objectif d’analyser l’évolution des thématiques abordées à la télévision au fil du temps. \n\n"
        "Vous pouvez en apprendre plus sur Open Data University [**ici**](https://defis.data.gouv.fr/opendatauniversity). \n\n"
        "Vous pouvez retrouver différents dashboards dans ce projet : \n\n"
        "- Analyse thématique : Permet d'avoir une vue d'ensemble afin d'analyser les thèmes avec possibilité de filtre un thème spécifique \n\n"
        "- Sciences : Focus sur le thème Sciences et techniques \n\n"
        "- Économie : Focus sur le thème Économie \n\n"
        "- TF1 : Focus sur la chaîne de télévision TF1 \n\n"
        "- Analyse Médias : Focus sur des évènements majeurs et leur impact sur la diffusion de leur thème \n\n"
        "- Comparaison thèmes : Permet de comparer 2 thèmes afin de voir leur différentes évolutions"
    )

if page == "Sciences":
    st.title("Dashboard : Analyse de l'évolution du thème Sciences à la télévision")

    col11, col12, col13 = st.columns(3)

    with col11:
        df_sciences_avg_duration = df_st.groupby("Année")["duree"].mean().reset_index()
        df_sciences_avg_duration.columns = ["Année", "duree_moyenne_secondes"]

        fig = px.bar(
            df_sciences_avg_duration,
            x="Année",
            y="duree_moyenne_secondes",
            title="Durée moyenne des reportages sur le theme 'Sciences'",
        )

        fig.update_layout(
            xaxis_title="Année",
            yaxis_title="Durée moyenne (en secondes)",
            template="plotly_white",
        )

        st.plotly_chart(fig, use_container_width=True)

    with col12:
        df_st_annee = df_st[df_st["Année"].isin([2000, 2020])]
        df_st_grouped = df_st_annee.groupby(["chaine", "Année"])["duree"].sum() / 3600
        df_st_grouped = df_st_grouped.reset_index()
        df_st_grouped.columns = ["chaine", "Année", "duree_totale_heures"]

        df_st_grouped["Année"] = df_st_grouped["Année"].astype(
            str
        )  ## Passer en str pour ne plus avoir la légende en dégradé et les barres cote à cote

        fig = px.bar(
            df_st_grouped,
            x="chaine",
            y="duree_totale_heures",
            color="Année",
            barmode="group",
            title="Comparaison du temps d'antenne du thème 'Sciences' en 2000 et 2020",
            color_discrete_map={
                "2000": "blue",
                "2020": "red",
            },
        )

        fig.update_layout(
            xaxis_title="Chaîne TV",
            yaxis_title="Durée totale des reportages (en heures)",
            template="plotly_white",
            xaxis=dict(tickangle=45),
            legend_title="Année",  # Titre de la légende
        )

        # Afficher dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with col13:
        df_sciences_chaines = df_st.groupby("chaine")["duree"].sum().reset_index()
        df_sciences_chaines.columns = ["chaine", "duree_totale"]

        fig = px.pie(
            df_sciences_chaines,
            names="chaine",
            values="duree_totale",
            title="Répartition du temps d'antenne du theme 'Sciences' par chaine",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col21, col22 = st.columns(2)

    with col21:
        # Convertir les données en DataFrame pour Plotly
        df_sciences_grouped = df_sciences_grouped.reset_index()
        df_sciences_grouped.columns = ["Année", "duree_totale_heures"]

        # Création du graphique interactif avec Plotly Express
        fig = px.line(
            df_sciences_grouped,
            x="Année",
            y="duree_totale_heures",
            markers=True,  # Ajoute des marqueurs sur la ligne
            line_shape="linear",
            title="Évolution de la durée d'apparition du theme Sciences",
        )

        # Personnalisation du style
        fig.update_traces(line=dict(color="blue"))  # Définir la couleur de la ligne
        fig.update_layout(
            xaxis_title="Année",
            yaxis_title="Durée totale des reportages (en heures)",
            xaxis=dict(dtick=2),  # Un tick tous les 2 ans
            template="plotly_white",  # Fond blanc plus moderne
        )

        # Afficher dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with col22:
        df_sciences_count = (
            df_st.groupby("Année").size().reset_index(name="Nombre de reportages")
        )

        # Création du graphique interactif avec Plotly Express
        fig = px.line(
            df_sciences_count,
            x="Année",
            y="Nombre de reportages",
            markers=True,  # Ajoute des marqueurs sur la ligne
            line_shape="linear",
            title="Évolution du nombre de reportages sur le theme Sciences",
        )

        # Personnalisation du style
        fig.update_traces(line=dict(color="green"))  # Définir la couleur de la ligne
        fig.update_layout(
            xaxis_title="Année",
            yaxis_title="Nombre de reportages",
            xaxis=dict(dtick=2),  # Un tick tous les 2 ans
            template="plotly_white",  # Fond blanc plus moderne
        )

        # Afficher dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

elif page == "TF1":
    st.title("Dashboard : Analyse de l'évolution de la chaîne de télévision TF1")

    df_tf1 = df[df["chaine"] == "TF1"]

    df_tf1_duree_theme = df_tf1.groupby("theme")["duree_heures"].sum().reset_index()
    df_tf1_duree_theme = df_tf1_duree_theme.sort_values(
        by="duree_heures", ascending=False
    )

    # Création du barplot avec Plotly Express
    fig = px.bar(
        df_tf1_duree_theme,
        x="theme",
        y="duree_heures",
        title="Temps total d'apparition des thèmes sur TF1",
        labels={"Durée (en heures)": "Durée totale (en heures)"},
        color_discrete_sequence=["#1f77b4"],
        text_auto=True,  # Afficher les valeurs sur les barres
    )

    # Personnalisation du layout
    fig.update_layout(
        xaxis_title="Thème",
        yaxis_title="Durée totale (en heures)",
        xaxis=dict(tickangle=45),  # Rotation des labels pour lisibilité
        template="plotly_white",
    )

    # Afficher dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("----")

    col21, col22 = st.columns(2)

    with col21:

        df_tf1_duree_moy = df_tf1.groupby("Année")["duree"].mean().reset_index()

        # Création du graphique
        fig = px.line(
            df_tf1_duree_moy,
            x="Année",
            y="duree",
            markers=True,
            title="Evolution du temps d'exposition moyen d'un sujet sur TF1",
            line_shape="linear",
        )

        # Mise en forme
        fig.update_traces(line=dict(color="red"), marker=dict(size=6))
        fig.update_layout(
            xaxis_title="Année",
            yaxis_title="Durée moyenne des reportages (en secondes)",
            template="plotly_white",
            xaxis=dict(tickmode="linear", dtick=2),  # Un tick tous les 2 ans
        )

        # Affichage dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with col22:
        df_tf1_count = (
            df[df["chaine"] == "TF1"]
            .groupby("Année")
            .size()
            .reset_index(name="Nombre de reportages")
        )

        # Créer le graphique avec Plotly
        fig = px.bar(
            df_tf1_count,
            x="Année",
            y="Nombre de reportages",
            text_auto=True,  # Afficher les valeurs sur les barres
            title="Évolution du nombre de sujets abordés sur TF1",
            color_discrete_sequence=["#1f77b4"],  # Bleu TF1
        )

        # Mise en forme
        fig.update_layout(
            xaxis_title="Année",
            yaxis_title="Nombre de reportages",
            template="plotly_white",
            xaxis=dict(tickangle=45),  # Incliner les labels si nécessaire
        )

        # Afficher dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

        df_tf1_theme = (
            df[df["chaine"] == "TF1"]
            .groupby(["Année", "theme"])["duree_heures"]
            .sum()
            .reset_index()
        )

    fig = px.line(
        df_tf1_theme,
        x="Année",
        y="duree_heures",
        color="theme",
        title="Évolution du temps d'antenne des thèmes sur TF1",
        markers=True,
    )

    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Durée totale (en heures)",
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)


elif page == "Analyse Thématique":
    st.title("Dashboard : Analyse Thématique des Sujets")
    # Initialisation du thème sélectionné dès le début
    if "theme_duration_selected" not in st.session_state:
        st.session_state.theme_duration_selected = df["theme"].unique()[0]

    # Première ligne : répartition globale + répartition annuelle
    col1, col2 = st.columns(2)

    with col1:

        if "theme" in df.columns:
            df_theme = df["theme"].value_counts().reset_index()
            df_theme.columns = ["theme", "count"]
            fig_bar = px.bar(
                df_theme,
                x="theme",
                y="count",
                labels={"count": "Nombre d'occurrences", "theme": "Thème"},
                title="Nombre total de sujets par thème",
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.error("La colonne 'theme' est manquante dans le dataset.")

    with col2:

        if (
            "theme" in df.columns
            and "nombre_sujets" in df.columns
            and "date" in df.columns
        ):
            df["year"] = df["date"].dt.year

            if "selected_year_state" not in st.session_state:
                st.session_state.selected_year_state = int(df["year"].max())

            selected_year = st.session_state.selected_year_state
            df_year = df[df["year"] == selected_year]

            if not df_year.empty:
                df_theme_pie = (
                    df_year.groupby("theme")["nombre_sujets"].sum().reset_index()
                )

                fig_pie = px.pie(
                    df_theme_pie,
                    values="nombre_sujets",
                    names="theme",
                    title=f"Répartition des thèmes en {selected_year}",
                    hole=0.3,
                )
                st.plotly_chart(fig_pie, use_container_width=True)

                # Slider en dessous du graphique
                selected_year = st.slider(
                    "📅 Choisissez une année :",
                    min_value=int(df["year"].min()),
                    max_value=int(df["year"].max()),
                    value=selected_year,
                    key="slider_theme_year",
                )
                st.session_state.selected_year_state = selected_year
            else:
                st.warning("Aucune donnée disponible pour cette année.")
        else:
            st.error("Colonnes manquantes pour l’analyse par année.")

    # Deuxième ligne : Thème par média + Évolution d’un thème
    col3, col4 = st.columns(2)

    with col3:

        if (
            "theme" in df.columns
            and "chaine" in df.columns
            and "nombre_sujets" in df.columns
        ):
            # Initialiser une valeur par défaut dans session_state si nécessaire
            if "theme_selected_col3" not in st.session_state:
                st.session_state.theme_selected_col3 = df["theme"].unique()[0]

            selected_theme_col3 = st.session_state.theme_selected_col3

            # Filtrage des données
            df_selected = df[df["theme"] == selected_theme_col3]

            if not df_selected.empty:
                df_theme_media = (
                    df_selected.groupby("chaine")["nombre_sujets"].sum().reset_index()
                )

                if not df_theme_media.empty:
                    fig_bar = px.bar(
                        df_theme_media,
                        x="chaine",
                        y="nombre_sujets",
                        title=f"Sujets sur '{selected_theme_col3}' par média (2000–2020)",
                        labels={
                            "chaine": "Chaîne",
                            "nombre_sujets": "Nombre de Sujets",
                        },
                        text="nombre_sujets",
                    )
                    fig_bar.update_traces(textposition="outside")
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.warning(
                        "Le thème existe, mais aucune donnée n'est associée à une chaîne."
                    )
            else:
                st.warning("Aucune donnée disponible pour ce thème.")

            # Selectbox EN BAS après le graphique
            selected_theme_col3 = st.selectbox(
                "🎯 Choisissez un thème à analyser :",
                df["theme"].unique(),
                index=list(df["theme"].unique()).index(selected_theme_col3),
                key="theme_select_col3",
            )

            # Met à jour la sélection dans session_state
            st.session_state.theme_selected_col3 = selected_theme_col3

    with col4:

        df["year"] = df["date"].dt.year

        if "theme_duration_selected" not in st.session_state:
            st.session_state.theme_duration_selected = df["theme"].unique()[0]

        selected_theme = st.session_state.theme_duration_selected

        df_theme_time = df[df["theme"] == selected_theme]
        df_theme_time = (
            df_theme_time.groupby("year")["duree_heures"].sum().reset_index()
        )
        df_theme_time["duree_smoothed"] = (
            df_theme_time["duree_heures"].rolling(window=3, min_periods=1).mean()
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df_theme_time["year"],
                y=df_theme_time["duree_heures"],
                mode="lines+markers",
                marker=dict(size=6, color="red"),
                line=dict(width=3, color="#1f77b4"),
                name="Durée totale",
            )
        )

        fig.update_layout(
            title=f"Évolution de la durée d'antenne pour '{selected_theme}' (2000–2020)",
            xaxis_title="Année",
            yaxis_title="Durée totale (en heures)",
            template="plotly_white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="lightgrey"),
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)

        # Sélecteur de thème en bas
        selected_theme = st.selectbox(
            "🎯 Choisissez un thème à analyser :",
            df["theme"].unique(),
            index=list(df["theme"].unique()).index(selected_theme),
            key="theme_duration_bottom",
        )

        st.session_state.theme_duration_selected = selected_theme


elif page == "Analyse Médias":
    st.title("🎬 Dashboard : Analyse par Média")

    # 📅 Dictionnaire des événements majeurs
    evenements_majeurs = {
        "Attentats du 11 septembre": "2001-09-11",
        "Crise financière de 2008": "2008-09-15",
        "Élection présidentielle France 2017": "2017-05-07",
        "Covid-19 (début OMS)": "2020-03-11",
        "Gilets Jaunes France": "2018-11-17",
        "COP21 (Accord de Paris)": "2015-12-12",
    }

    # Sélection des filtres (affichés en bas mais déclarés ici)
    col_ev, col_med = st.columns([2, 1])

    with col_ev:
        selected_event = st.selectbox(
            "🗓️ Sélectionnez un événement :",
            list(evenements_majeurs.keys()),
            key="event_selector",
        )

    with col_med:
        selected_media = st.selectbox(
            "📺 Sélectionnez un média :", df["chaine"].unique(), key="media_selector"
        )

    # Calcul des périodes
    event_date = pd.to_datetime(evenements_majeurs[selected_event])
    periode_avant = event_date - pd.DateOffset(months=6)
    periode_apres = event_date + pd.DateOffset(months=6)

    # Création des colonnes de visualisation
    col1, col2 = st.columns(2)

    with col1:
        # Filtrage média + période
        df_event = df[(df["date"] >= periode_avant) & (df["date"] <= periode_apres)]
        df_event = df_event[df_event["chaine"] == selected_media]

        # Avant / après
        df_event["periode"] = df_event["date"].apply(
            lambda x: "Avant" if x < event_date else "Après"
        )
        df_event_time = (
            df_event.groupby(["periode", "theme"])["duree_heures"].sum().reset_index()
        )

        # Graphique
        fig_event = px.bar(
            df_event_time,
            x="periode",
            y="duree_heures",
            color="theme",
            title=f"Couverture de '{selected_event}' sur {selected_media}",
            labels={
                "periode": "Période",
                "duree": "Durée totale (s)",
                "theme": "Thème",
            },
            text_auto=".2s",
            barmode="stack",
        )

        fig_event.update_layout(
            template="plotly_white",
            xaxis_title="Période",
            yaxis_title="Durée totale (en heures)",
            yaxis=dict(gridcolor="lightgrey"),
            legend_title="Thème",
        )

        st.plotly_chart(fig_event, use_container_width=True)

    with col2:

        #  Associer chaque événement à une thématique clé
        theme_evenement = {
            "Attentats du 11 septembre": "International",
            "Crise financière de 2008": "Économie",
            "Élection présidentielle France 2017": "Politique France",
            "Covid-19 (début OMS)": "Santé",
            "Gilets Jaunes France": "Société",
            "COP21 (Accord de Paris)": "Environnement",
        }

        # Récupérer le thème associé à l'événement sélectionné
        if selected_event in theme_evenement:
            theme_associe = theme_evenement[selected_event]

        # Filtrer sur la période + thématique associée
        df_event_theme = df[
            (df["date"] >= periode_avant)
            & (df["date"] <= periode_apres)
            & (df["theme"] == theme_associe)
        ]

        df_theme_par_chaine = (
            df_event_theme.groupby("chaine")["duree_heures"].sum().reset_index()
        )
        df_theme_par_chaine = df_theme_par_chaine.sort_values(
            by="duree_heures", ascending=False
        )

        # Graphe
        fig_theme_chaine = px.bar(
            df_theme_par_chaine,
            x="chaine",
            y="duree_heures",
            title=f"Durée d’exposition au thème '{theme_associe}' autour de l’événement '{selected_event}'",
            labels={"chaine": "Chaîne", "duree": "Durée totale (en heures)"},
            color="chaine",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )

        fig_theme_chaine.update_layout(
            template="plotly_white",
            yaxis_title="Durée totale (en heures)",
            xaxis_title="Chaîne TV",
            yaxis=dict(gridcolor="lightgrey"),
            showlegend=False,
        )

        st.plotly_chart(fig_theme_chaine, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:

            # Récupérer les données dans la même période que les autres graphiques
            df_event_global = df[
                (df["date"] >= periode_avant) & (df["date"] <= periode_apres)
            ]

            # Agréger la durée par thème
            df_theme_duree = (
                df_event_global.groupby("theme")["duree_heures"].sum().reset_index()
            )
            df_theme_duree = df_theme_duree.sort_values(
                by="duree_heures", ascending=False
            )

            # Graphique à barres (top 10)
            fig_theme_bar = px.bar(
                df_theme_duree.head(10),
                x="theme",
                y="duree_heures",
                title=f"Thèmes dominants autour de '{selected_event}' (toutes chaînes)",
                labels={"theme": "Thème", "duree_heures": "Durée totale (en heures)"},
                color="theme",
                color_discrete_sequence=px.colors.qualitative.Set3,
            )

            fig_theme_bar.update_layout(
                template="plotly_white",
                xaxis_title="Thème",
                yaxis_title="Durée totale d’antenne (en heures)",
                yaxis=dict(gridcolor="lightgrey"),
                xaxis=dict(tickangle=30),
                showlegend=False,
            )

            st.plotly_chart(fig_theme_bar, use_container_width=True)


elif page == "Économie":
    st.title("💼 Dashboard : Couverture du thème Économie")

    #  Préparation des données
    df_economie = df[df["theme"] == "Economie"].copy()
    df_economie["Année"] = df_economie["date"].dt.year
    df_economie["Mois"] = df_economie["date"].dt.to_period("M").astype(str)

    # --------- Graph 1 : Scatter sujets vs durée ---------
    df_scatter = (
        df_economie.groupby("chaine")
        .agg(total_duree=("duree_heures", "sum"), nb_sujets=("nombre_sujets", "sum"))
        .reset_index()
    )

    fig1 = px.scatter(
        df_scatter,
        x="nb_sujets",
        y="total_duree",
        text="chaine",
        size="total_duree",
        color="chaine",
        labels={
            "nb_sujets": "Nombre de sujets",
            "total_duree": "Durée totale (en heures)",
            "chaine": "Chaîne",
        },
        title="Nombre de sujets vs Durée totale par chaîne (Économie)",
    )
    fig1.update_traces(textposition="top center")
    fig1.update_layout(template="plotly_white", hovermode="closest")

    # --------- Graph 2 : Durée moyenne par sujet ---------
    df2 = df_economie.groupby("Année")["duree"].mean().reset_index()
    fig2 = px.bar(
        df2,
        x="Année",
        y="duree",
        title="Durée moyenne par sujet économique",
        labels={"duree": "Durée moyenne (s)", "Année": "Année"},
    )

    # --------- Graph 3 : Répartition des chaînes ---------
    df3 = df_economie.groupby("chaine")["duree"].sum().reset_index()
    fig3 = px.pie(
        df3,
        names="chaine",
        values="duree",
        title="Répartition des sujets économiques par chaîne",
    )

    # --------- Affichage ligne 1 ---------
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # --------- Graph 4 : Classement des chaînes ---------
    df4 = (
        df_economie.groupby("chaine")["duree_heures"]
        .sum()
        .reset_index()
        .sort_values(by="duree_heures", ascending=True)
    )
    fig4 = px.bar(
        df4,
        x="duree_heures",
        y="chaine",
        orientation="h",
        title="Durée totale d'antenne par chaîne (Économie)",
        labels={"duree_heures": "Durée totale (en heures)", "chaine": "Chaîne"},
        color="duree_heures",
        color_continuous_scale="Viridis",
    )

    # --------- Graph 5 : Évolution des top chaînes ---------
    df5 = df_economie.groupby(["Année", "chaine"])["duree_heures"].sum().reset_index()
    top_chaines = df4["chaine"].tail(5).tolist()
    df_top = df5[df5["chaine"].isin(top_chaines)]

    fig5 = px.line(
        df_top,
        x="Année",
        y="duree_heures",
        color="chaine",
        markers=True,
        title="Évolution annuelle des chaînes les plus actives (Économie)",
        labels={
            "duree_heures": "Durée totale (en heures)",
            "Année": "Année",
            "chaine": "Chaîne",
        },
    )
    fig5.update_layout(template="plotly_white", hovermode="x unified")

    # --------- Affichage ligne 2 ---------
    col4, col5 = st.columns(2)
    with col4:
        st.plotly_chart(fig4, use_container_width=True)
    with col5:
        st.plotly_chart(fig5, use_container_width=True)


elif page == "Comparaison Thèmes":
    st.title("🔍 Dashboard : Comparaison entre deux thèmes télévisés")

    # 🎛️ Sélection des deux thèmes
    all_themes = df["theme"].dropna().unique()
    col_select1, col_select2 = st.columns(2)

    with col_select1:
        theme1 = st.selectbox(
            "📌 Choisissez le premier thème", sorted(all_themes), key="theme1"
        )
    with col_select2:
        theme2 = st.selectbox(
            "📌 Choisissez le second thème", sorted(all_themes), index=1, key="theme2"
        )

    # Filtrage
    df1 = df[df["theme"] == theme1].copy()
    df2 = df[df["theme"] == theme2].copy()

    df1["Année"] = df1["date"].dt.year
    df2["Année"] = df2["date"].dt.year

    # ---------- GRAPHIQUE 1 : Évolution durée ----------
    df_duree = (
        pd.concat([df1, df2])
        .groupby(["Année", "theme"])["duree_heures"]
        .sum()
        .reset_index()
    )

    fig_duree = px.line(
        df_duree,
        x="Année",
        y="duree_heures",
        color="theme",
        markers=True,
        title="Évolution de la durée d’antenne",
        labels={
            "duree_heures": "Durée totale (en heures)",
            "Année": "Année",
            "theme": "Thème",
        },
    )
    fig_duree.update_layout(template="plotly_white", hovermode="x unified")

    # ---------- GRAPHIQUE 2 : Nombre de sujets ----------
    df_count = (
        pd.concat([df1, df2])
        .groupby(["Année", "theme"])
        .size()
        .reset_index(name="nombre_sujets")
    )

    fig_count = px.bar(
        df_count,
        x="Année",
        y="nombre_sujets",
        color="theme",
        barmode="group",
        title="Nombre de sujets par année",
        labels={
            "nombre_sujets": "Nombre de sujets",
            "Année": "Année",
            "theme": "Thème",
        },
    )
    fig_count.update_layout(template="plotly_white")

    # --------- Affichage côte à côte ---------
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.plotly_chart(fig_duree, use_container_width=True)
    with col_g2:
        st.plotly_chart(fig_count, use_container_width=True)

    st.markdown("---")

    # ---------- GRAPHIQUE 3 : Classement des chaînes ----------
    st.subheader("📺 Classement des chaînes par durée pour chaque thème")

    col3, col4 = st.columns(2)

    with col3:
        top_chaine1 = (
            df1.groupby("chaine")["duree_heures"]
            .sum()
            .reset_index()
            .sort_values(by="duree_heures", ascending=False)
        )
        fig_chaine1 = px.bar(
            top_chaine1.head(5),
            x="chaine",
            y="duree_heures",
            title=f"🏆 Top chaînes - {theme1}",
            labels={"chaine": "Chaîne", "duree_heures": "Durée totale (en heures)"},
            color="chaine",
        )
        st.plotly_chart(fig_chaine1, use_container_width=True)

    with col4:
        top_chaine2 = (
            df2.groupby("chaine")["duree_heures"]
            .sum()
            .reset_index()
            .sort_values(by="duree_heures", ascending=False)
        )
        fig_chaine2 = px.bar(
            top_chaine2.head(5),
            x="chaine",
            y="duree_heures",
            title=f"🏆 Top chaînes - {theme2}",
            labels={"chaine": "Chaîne", "duree_heures": "Durée totale (en heures)"},
            color="chaine",
        )
        st.plotly_chart(fig_chaine2, use_container_width=True)
