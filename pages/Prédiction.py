import streamlit as st
import pickle
import pandas as pd
from supabase import create_client
import os
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
from utils import *
import requests
import json



# Charger les données et le modèle
df_reg = pd.read_csv("data/regions-france.csv")
# with open("xgb.pkl", "rb") as file:
#     model = pickle.load(file)


# Créer un client Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Définir la mise en page
st.set_page_config(layout="wide")

# Charger le CSS personnalisé
css = load_css()
st.markdown(css, unsafe_allow_html=True)

# Afficher le logo
st.markdown(f"<p style='text-align: center;'>{img_to_html('data/M1.png')}</p>", unsafe_allow_html=True)

# Définir les colonnes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
    """
    <style>
        .stContainer {
            color: #F1EFE7;
        }
    </style>
    """,
    unsafe_allow_html=True
)

    st.title('')
    with st.container(border=True):
        region_code_map = dict(zip(df_reg['nom_region'], df_reg['code_region']))
        selected_region = st.selectbox("Sélectionnez une région", df_reg['nom_region'])
        selected_region_code = region_code_map[selected_region]

        data = {
            "Code postal_x" : st.number_input("**Code postal**", value=None),
            "Surface Carrez du 1er lot" : st.number_input("**Surface Carrez**"),
            "Nombre pieces principales" : st.number_input("**Nombre pieces principales**"),
            "code_region" : selected_region_code,
        }
        data = pd.DataFrame(data, index=["1"])


# Bouton pour effectuer la prédiction
if st.button("Prediction"):
    response = requests.get(
    f'https://api-e1-2.onrender.com/predict?Code_postal_x={data["Code postal_x"][0]}&Surface_Carrez_du_1er_lot={data["Surface Carrez du 1er lot"][0]}&Nombre_pieces_principales={data["Nombre pieces principales"][0]}&code_region={data["code_region"][0]}'
)

    pred = json.loads(response.content.decode("utf-8"))["result"][0]
    m2 = data["Surface Carrez du 1er lot"].astype(float).values
    mean = pred / m2
    st.write(data["Nombre pieces principales"][0])
    with col2:
        st.title('Résultats')
        st.info('Prédiction du prix:')
        st.success(f"{round(pred)} €")
        st.info('Prix au M2:')
        st.success(f'{round(mean[0], 2)} €')
    with col3:
        st.title("")
        st.title("")
        st.title("")
        st.title("")
        st.title("")
        if 2800 < pred / m2 < 3400:
            st.markdown("<div style='text-align: center;'><span style='color: #FFD700; font-size: 48px;'>👌</span><br> Prix moyen</div>", unsafe_allow_html=True)
        elif pred / m2 > 4000:
            st.markdown("<div style='text-align: center;'><span style='color: #FF0000; font-size: 48px;'>🔴</span><br> Prix élevé</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center;'><span style='color: #008000; font-size: 48px;'>✅</span><br> Bon prix</div>", unsafe_allow_html=True)

# Bouton pour enregistrer les données

if st.button("Enregistrer"):
    data = supabase.table('prediction').insert({"Code postal_x": data["Code postal_x"][0],
                                                "Surface Carrez du 1er lot": m2[0],
                                                "Nombre pieces principales": data["Nombre pieces principales"][0],
                                                "Pred": float(pred)}).execute()



# Récupérer les données de la table depuis la base de données
df_pred = supabase.table("prediction").select("*").execute()

df_pred = pd.DataFrame(df_pred)
df_pred = df_pred[1].iloc[0]
df_pred = pd.DataFrame(df_pred)

st.title("")
st.write("Apercu de la table prédiction")
st.table(df_pred.tail())
