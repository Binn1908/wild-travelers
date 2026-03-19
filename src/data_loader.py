import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import streamlit as st

DATA_DIR = Path(__file__).parent.parent / "data"


@st.cache_data
def load_df_etablissements() -> pd.DataFrame:
    """
    Charge et concatène les 4 fichiers pickle du jeu de données principal.
    Contient uniquement les catégories Hébergement et Restauration.
    """
    parties = [
        pd.read_pickle(DATA_DIR / f"df_etablissements_{i}.pickle") for i in range(1, 5)
    ]
    return pd.concat(parties, ignore_index=True)


@st.cache_data
def load_df_autres() -> pd.DataFrame:
    """
    Charge le jeu de données secondaire (CSV).
    Contient les catégories Hébergement/Restauration et Autres.
    """
    return pd.read_csv(DATA_DIR / "df_autres.csv")


@st.cache_data
def load_ml1(
    _df_autres: pd.DataFrame,
) -> tuple[TfidfVectorizer, LogisticRegression]:
    """
    Entraîne le modèle ML 1 : détecte si un établissement appartient
    à la catégorie Autres ou non.
    Le préfixe _ sur _df_autres indique à Streamlit de ne pas hasher ce paramètre.
    """
    df_autres = _df_autres.copy()
    df_autres["description_pretraitee"] = df_autres["description_pretraitee"].astype(
        str
    )

    X_train, _, y_train, _ = train_test_split(
        df_autres["description_pretraitee"],
        df_autres["category"],
        test_size=0.25,
        random_state=42,
    )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2),
        min_df=5,
    )
    X_train_vectorized = vectorizer.fit_transform(X_train)

    model = LogisticRegression(class_weight="balanced")
    model.fit(X_train_vectorized, y_train)

    return vectorizer, model


@st.cache_data
def load_ml2(
    _df_etablissements: pd.DataFrame,
) -> tuple[TfidfVectorizer, LogisticRegression]:
    """
    Entraîne le modèle ML 2 : détecte si un établissement est un
    Hébergement ou une Restauration.
    Le préfixe _ sur _df_etablissements indique à Streamlit de ne pas hasher ce paramètre.
    """
    X_train, _, y_train, _ = train_test_split(
        _df_etablissements["description_pretraitee"],
        _df_etablissements["category"],
        test_size=0.2,
        random_state=42,
    )

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=5,
    )
    X_train_vectorized = vectorizer.fit_transform(X_train)

    model = LogisticRegression(class_weight="balanced", max_iter=1000)
    model.fit(X_train_vectorized, y_train)

    return vectorizer, model
