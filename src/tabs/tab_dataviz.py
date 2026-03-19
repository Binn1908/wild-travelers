import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


def _kpi_etablissements_par_region(df: pd.DataFrame) -> None:
    """
    Heatmap : nombre d'établissements par région et catégorie.
    """
    st.subheader("Nombre d'établissements par région et catégorie")

    etablissements_par_region = (
        df.groupby(["region", "category"]).size().unstack(fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(etablissements_par_region, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def _kpi_distribution_categories(df: pd.DataFrame) -> None:
    """
    Camembert : distribution des établissements par catégorie.
    """
    st.subheader("Distribution des établissements par catégorie")

    nombre_par_categorie = df["category"].value_counts()
    couleurs = sns.color_palette("pastel")[: len(nombre_par_categorie)]

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        nombre_par_categorie,
        labels=nombre_par_categorie.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=couleurs,
        textprops={"fontsize": 12},
    )
    ax.add_artist(plt.Circle((0, 0), 0.7, color="white"))
    ax.axis("equal")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig)
    plt.close(fig)


def _kpi_acces_mobilite_reduite(df: pd.DataFrame) -> None:
    """
    Camembert : répartition des établissements avec accès mobilité réduite.
    """
    st.subheader("Répartition des établissements avec accès mobilité réduite")

    nombre_acces = df["reducedMobilityAccess"].value_counts()
    couleurs = ["#EEB1B2", "#AAD7AA"]

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        nombre_acces,
        labels=nombre_acces.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=couleurs,
        textprops={"fontsize": 8},
    )
    ax.add_artist(plt.Circle((0, 0), 0.7, fc="white"))
    ax.axis("equal")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig)
    plt.close(fig)


def _kpi_top10_villes(df: pd.DataFrame) -> None:
    """
    Barplot horizontal : top 10 des villes avec le plus d'établissements.
    """
    st.subheader("Top 10 des villes avec le plus d'établissements")

    top10_villes = df["ville"].value_counts().nlargest(10)
    couleurs = sns.color_palette("pastel", len(top10_villes))

    fig, ax = plt.subplots(figsize=(6, 2))
    sns.barplot(x=top10_villes.values, y=top10_villes.index, palette=couleurs, ax=ax)
    ax.set_xlabel("Nombre d'établissements", fontsize=8)
    ax.set_ylabel("")

    for i, valeur in enumerate(top10_villes.values):
        ax.text(
            valeur + 0.2, i, str(valeur), color="black", fontweight="bold", fontsize=8
        )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def render(df: pd.DataFrame) -> None:
    """
    Affiche les 4 visualisations du jeu de données établissements.
    """

    _kpi_etablissements_par_region(df)
    _kpi_distribution_categories(df)
    _kpi_acces_mobilite_reduite(df)
    _kpi_top10_villes(df)
