import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Téléchargement conditionnel des ressources NLTK
for ressource, chemin in [
    ("stopwords", "corpora/stopwords"),
    ("punkt_tab", "tokenizers/punkt_tab"),
]:
    try:
        nltk.data.find(chemin)
    except LookupError:
        nltk.download(ressource, quiet=True)

# Définir la liste des mots vides (stop words) en français
_stop_words = set(stopwords.words("french"))

# Définir le stemmer pour la racinisation (stemming)
_stemmer = SnowballStemmer("french")


def preprocess_text(texte: str) -> str:
    """
    Prétraite un texte en vue d'une classification NLP :
    mise en minuscules, suppression de la ponctuation et des caractères
    spéciaux, tokenisation, suppression des stop words et racinisation.

    Retourne une chaîne vide si l'entrée n'est pas une chaîne valide.
    """
    if not isinstance(texte, str):
        return ""

    texte = texte.lower()

    # Supprimer tout sauf a-z et espaces
    texte = re.sub(r"[^a-z ]", "", texte)

    # Tokenization des mots
    mots = nltk.word_tokenize(texte)

    # Supprimer les mots vides
    mots = [mot for mot in mots if mot not in _stop_words]

    # Appliquer le stemming
    mots = [_stemmer.stem(mot) for mot in mots]

    # Joindre les mots en une seule chaîne de caractères
    return " ".join(mots)
