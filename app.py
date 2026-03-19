from src.data_loader import (
    load_df_autres,
    load_df_etablissements,
    load_ml1,
    load_ml2,
)
from pathlib import Path
from PIL import Image
import streamlit as st
from src.tabs import tab_dataviz, tab_home, tab_ml

st.set_page_config(layout="wide")

# ── Chargement des données ────────────────────────────────────────────────────

df_etablissements = load_df_etablissements()
df_autres = load_df_autres()
vectorizer1, model1 = load_ml1(_df_autres=df_autres)
vectorizer2, model2 = load_ml2(_df_etablissements=df_etablissements)

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    logo = Image.open(Path(__file__).parent / "assets" / "logo.png")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, width=100)

    st.header("Filtres")

    CATEGORIES = ["Hébergement", "Restauration"]
    user_type = st.multiselect("Type d'établissement", CATEGORIES)
    user_mobility = st.checkbox("Accès mobilité réduite")

    # Région
    region_options = df_etablissements["region"].drop_duplicates().tolist()
    region_options.remove("Île-de-France")
    region_options.insert(0, "Île-de-France")
    user_region = st.selectbox("Région", region_options)

    # Département
    dep_options = ["Tous"] + (
        df_etablissements.loc[df_etablissements["region"] == user_region]["departement"]
        .drop_duplicates()
        .tolist()
    )
    user_dep = st.selectbox("Département", dep_options)

    # Ville — uniquement si un département est sélectionné
    if user_dep != "Tous":
        city_options = ["Tous"] + (
            df_etablissements.loc[df_etablissements["departement"] == user_dep]["ville"]
            .drop_duplicates()
            .tolist()
        )
        user_city = st.selectbox("Ville", city_options)
    else:
        user_city = "Tous"

# ── Contenu principal ─────────────────────────────────────────────────────────

st.header("Bienvenue chez Wild Travelers")

tab1, tab2, tab3 = st.tabs(["🗺️ Home", "📊 Dataviz", "🤖 Modèle ML"])

with tab1:
    tab_home.render(
        df=df_etablissements,
        user_type=user_type,
        user_region=user_region,
        user_dep=user_dep,
        user_city=user_city,
        user_mobility=user_mobility,
    )

with tab2:
    tab_dataviz.render(df=df_etablissements)

with tab3:
    tab_ml.render(
        vectorizer1=vectorizer1,
        model1=model1,
        vectorizer2=vectorizer2,
        model2=model2,
    )

# ── Footer ────────────────────────────────────────────────────────────────────

st.divider()
st.markdown(
    "**Wild Travelers** · "
    "Réalisé par [Chinnawat Wisetwongsa](https://linkedin.com/in/wisetwongsa/)"
)
