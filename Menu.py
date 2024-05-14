import streamlit as st
from utils import *
from dotenv import load_dotenv
load_dotenv()


# Définir la mise en page
st.set_page_config(layout="wide")

# Charger le CSS personnalisé
css = load_css()
st.markdown(css, unsafe_allow_html=True)

# Afficher le logo
st.markdown(f"<p style='text-align: center;'>{img_to_html('data/M1.png')}</p>", unsafe_allow_html=True)

st.write("""
# Bienvenue sur IA.ppart!

Ce projet a été réalisé dans le cadre de mon projet de fin d'études, avec pour objectif de fournir un outil d'aide à la décision pour la réalisation d'achat ou de vente d'appartements en France.

Que vous soyez un acheteur potentiel cherchant à évaluer le juste prix d'une propriété ou un vendeur souhaitant maximiser le rendement de votre investissement, notre application est conçue pour vous fournir les informations et les analyses nécessaires pour prendre des décisions éclairées.

Grâce à des algorithmes de prédiction avancés et à une analyse approfondie des données immobilières, notre application peut vous aider à estimer les prix de vente des appartements, à identifier les tendances du marché et à explorer les caractéristiques qui influent sur la valeur des biens immobiliers.

Nous sommes ravis de vous accueillir et espérons que notre application vous sera utile dans votre parcours immobilier.

N'hésitez pas à explorer les fonctionnalités disponibles et à nous faire part de vos commentaires et suggestions pour améliorer notre service.

Bonne exploration !
""")
