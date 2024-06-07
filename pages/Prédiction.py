import streamlit as st
import pandas as pd
from supabase import create_client
import requests
import json
from utils import load_css, img_to_html

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
            "Code postal_x": st.number_input("**Code postal**", value=0, format='%d'),
            "Surface Carrez du 1er lot": st.number_input("**Surface Carrez**", value=0.0, format='%f'),
            "Nombre pieces principales": st.number_input("**Nombre pieces principales**", value=0, format='%d'),
            "code_region": selected_region_code,
        }
        data = pd.DataFrame(data, index=["1"])

# Initialiser les variables de session
if 'pred' not in st.session_state:
    st.session_state['pred'] = None
if 'm2' not in st.session_state:
    st.session_state['m2'] = None

# Bouton pour effectuer la prédiction
if st.button("Prediction"):
    try:
        response = requests.get(
            f'https://api-e1-2.onrender.com/predict?Code_postal_x={data["Code postal_x"][0]}&Surface_Carrez_du_1er_lot={data["Surface Carrez du 1er lot"][0]}&Nombre_pieces_principales={data["Nombre pieces principales"][0]}&code_region={data["code_region"][0]}'
        )
        response.raise_for_status()  # Ensure we handle HTTP errors
        response_content = response.content.decode("utf-8")


        result = json.loads(response_content)["result"]
        if result:  # Ensure result is not empty
            st.session_state['pred'] = result[0]
            st.session_state['m2'] = data["Surface Carrez du 1er lot"].astype(float).values
            mean = st.session_state['pred'] / st.session_state['m2']

            with col2:
                st.title('Résultats')
                st.info('Prédiction du prix:')
                st.success(f"{round(st.session_state['pred'])} €")
                st.info('Prix au M2:')
                st.success(f'{round(mean[0], 2)} €')
            with col3:
                st.title("")
                st.title("")
                st.title("")
                st.title("")
                st.title("")
                if 2800 < st.session_state['pred'] / st.session_state['m2'] < 3400:
                    st.markdown("<div style='text-align: center;'><span style='color: #FFD700; font-size: 48px;'>👌</span><br> Prix moyen</div>", unsafe_allow_html=True)
                elif st.session_state['pred'] / st.session_state['m2'] > 4000:
                    st.markdown("<div style='text-align: center;'><span style='color: #FF0000; font-size: 48px;'>🔴</span><br> Prix élevé</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center;'><span style='color: #008000; font-size: 48px;'>✅</span><br> Bon prix</div>", unsafe_allow_html=True)
        else:
            st.error("Résultat vide de l'API")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")

# Bouton pour enregistrer les données
if st.button("Enregistrer"):
    if st.session_state['pred'] is not None and st.session_state['m2'] is not None:
        try:
            # Convertir les valeurs en types natifs Python
            record = {
                "Code postal_x": int(data["Code postal_x"][0]),
                "Surface Carrez du 1er lot": float(st.session_state['m2'][0]),
                "Nombre pieces principales": int(data["Nombre pieces principales"][0]),
                "Pred": float(st.session_state['pred'])
            }
            supabase.table('prediction').insert(record).execute()
            st.success("Données enregistrées avec succès")
        except Exception as e:
            st.error(f"Erreur lors de l'enregistrement des données : {e}")
    else:
        st.error("Veuillez effectuer une prédiction avant d'enregistrer.")

# Récupérer les données de la table depuis la base de données
try:
    df_pred = supabase.table("prediction").select("*").execute()
    df_pred = pd.DataFrame(df_pred)
    df_pred = df_pred[1].iloc[0]
    df_pred = pd.DataFrame(df_pred)

    st.title("")
    st.write("Aperçu de la table prédiction")
    st.table(df_pred.tail())
except Exception as e:
    st.error(f"Erreur lors de la récupération des données : {e}")
