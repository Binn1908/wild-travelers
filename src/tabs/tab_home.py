import pandas as pd
import pydeck as pdk
import streamlit as st

COLONNES_AFFICHAGE = [
    "nom_etablissement",
    "category",
    "latitude",
    "longitude",
    "rue",
    "code_postal",
    "ville",
    "telephone",
    "site_web",
]

# Coordonnées par défaut : Paris
LAT_DEFAUT = 48.856578
LON_DEFAUT = 2.351828

ICON_HOTEL_URL = "https://raw.githubusercontent.com/Binn1908/wild-travelers/main/assets/icon_hotel.png"
ICON_RESTO_URL = "https://raw.githubusercontent.com/Binn1908/wild-travelers/main/assets/icon_resto.png"

ICON_HOTEL = {"url": ICON_HOTEL_URL, "width": 242, "height": 242, "anchorY": 242}
ICON_RESTO = {"url": ICON_RESTO_URL, "width": 242, "height": 242, "anchorY": 242}


def render(
    df: pd.DataFrame,
    user_type: list[str],
    user_region: str,
    user_dep: str,
    user_city: str,
    user_mobility: bool,
) -> None:
    """
    Affiche la carte interactive des établissements filtrés.
    """
    df_carte = df.loc[df["region"] == user_region].copy()

    if user_dep != "Tous":
        df_carte = df_carte.loc[df_carte["departement"] == user_dep]

    if user_city != "Tous":
        df_carte = df_carte.loc[df_carte["ville"] == user_city]

    if user_type:
        df_carte = df_carte.loc[df_carte["category"].isin(user_type)]

    if user_mobility:
        df_carte = df_carte.loc[df_carte["reducedMobilityAccess"] == True]

    df_carte = df_carte[COLONNES_AFFICHAGE]

    if len(df_carte) > 0:
        st.metric("Établissements trouvés :", len(df_carte))
        lat_centre = df_carte["latitude"].mean()
        lon_centre = df_carte["longitude"].mean()
    else:
        st.info("Aucun établissement trouvé pour cette sélection.")
        lat_centre = LAT_DEFAUT
        lon_centre = LON_DEFAUT

    df_carte["icon_data"] = df_carte["category"].apply(
        lambda cat: ICON_HOTEL if cat == "Hébergement" else ICON_RESTO
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style="road",
            initial_view_state=pdk.ViewState(
                latitude=lat_centre,
                longitude=lon_centre,
                zoom=9,
                pitch=40,
            ),
            layers=[
                pdk.Layer(
                    type="IconLayer",
                    data=df_carte,
                    get_icon="icon_data",
                    get_size=1,
                    size_scale=15,
                    get_position=["longitude", "latitude"],
                    pickable=True,
                ),
            ],
            tooltip={
                "html": (
                    "<b>Nom :</b> {nom_etablissement}<br/>"
                    "<b>Type :</b> {category}<br/>"
                    "<b>Adresse :</b> {rue}, {code_postal} {ville}<br/>"
                    "<b>Téléphone :</b> {telephone}<br/>"
                    "<b>Site web :</b> {site_web}"
                ),
                "style": {"color": "white"},
            },
        )
    )
