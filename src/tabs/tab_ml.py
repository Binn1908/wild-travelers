from ..nlp import preprocess_text
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import streamlit as st

DESCRIPTION_EXEMPLE = "Profitez de nos chambres confortables avec vue sur la mer et petit-déjeuner inclus."
SEUIL_INCERTITUDE_BAS = 0.3
SEUIL_INCERTITUDE_HAUT = 0.7


def render(
    vectorizer1: TfidfVectorizer,
    model1: LogisticRegression,
    vectorizer2: TfidfVectorizer,
    model2: LogisticRegression,
) -> None:
    """
    Affiche l'interface de prédiction du type d'établissement.
    """

    st.subheader("Test du modèle")

    description = st.text_area(
        "Veuillez renseigner une description :",
        value=DESCRIPTION_EXEMPLE,
    )

    texte_pretraite = preprocess_text(description)

    # Modèle 1 : détecte si l'établissement appartient à la catégorie Autres
    texte_vectorise1 = vectorizer1.transform([texte_pretraite])
    prediction1 = model1.predict(texte_vectorise1)[0]

    if prediction1 == "Autres":
        st.write(f"Prédiction du type d'établissement : **{prediction1}**")
        return

    # Modèle 2 : distingue Hébergement et Restauration
    texte_vectorise2 = vectorizer2.transform([texte_pretraite])
    prediction2 = model2.predict(texte_vectorise2)[0]
    probabilites = model2.predict_proba(texte_vectorise2)[0]

    # Si la probabilité est trop proche de 50/50, on indique l'incertitude
    if SEUIL_INCERTITUDE_BAS <= probabilites[0] <= SEUIL_INCERTITUDE_HAUT:
        prediction2 = "Hébergement / Restauration"

    st.write(f"Prédiction du type d'établissement : **{prediction2}**")
