import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import learning_curve
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
import base64
from pathlib import Path
import streamlit as st

def alldrop(df):
    df = df.drop_duplicates()
    df = df.dropna(subset = "Surface Carrez du 1er lot")
    df_drop= df.drop(["Code service sages", "Reference document", "1 Articles CGI","2 Articles CGI",
            "3 Articles CGI","4 Articles CGI","5 Articles CGI","Section","No disposition",
            "Nature culture","Nature culture speciale","Identifiant local","Prefixe de section","Surface Carrez du 2eme lot","2eme lot",
                "3eme lot","4eme lot","5eme lot","No Volume","1er lot","No plan","Surface terrain","Surface reelle bati","Nombre de lots","B/T/Q",
            "Surface Carrez du 3eme lot","Surface Carrez du 4eme lot","Surface Carrez du 5eme lot","Code type local","Nature mutation"],axis = 1)
    return df_drop


def cleaner(df_drop):
    df_drop = df_drop.reset_index(drop = True)
    df_drop["id_vente"] = df_drop.index+1
    df_drop["Date mutation"] = pd.to_datetime(df_drop["Date mutation"],format="%d/%m/%Y")
    df_drop["Valeur fonciere"] = df_drop["Valeur fonciere"].str.replace(',','.')
    df_drop["Valeur fonciere"] = df_drop["Valeur fonciere"].astype(float)
    df_drop["Surface Carrez du 1er lot"] = df_drop["Surface Carrez du 1er lot"].str.replace(',','.')
    df_drop["Surface Carrez du 1er lot"] = df_drop["Surface Carrez du 1er lot"].astype(float)
    df_drop["Commune"] = df_drop["Commune"].astype("string")
    df_drop["Type local"] = df_drop["Type local"].astype("string")
    df_drop["Code departement"] = df_drop["Code departement"].astype("string")
    df_clean = df_drop
    return df_clean


def drop2(df_clean):
    df_clean = df_clean.dropna()
    return df_clean


# Création d'une fonction pour afficher la courbe d'apprentissage
def plot_learning_curve(estimator, X, y):
    train_sizes, train_scores, test_scores, fit_times, _ = learning_curve(
        estimator, X, y, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10), scoring='neg_mean_squared_error',
        return_times=True
    )

    train_scores_mean = -np.mean(train_scores, axis=1)
    test_scores_mean = -np.mean(test_scores, axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_scores_mean, label='Train')
    plt.plot(train_sizes, test_scores_mean, label='Test')
    plt.xlabel('Taille de l\'échantillon d\'apprentissage')
    plt.ylabel('Erreur quadratique moyenne')
    plt.title('Courbe d\'apprentissage pour XGBoost')
    plt.legend()
    plt.show()


def training_xgb(df_clean):
    X = df_clean.drop(columns=["Valeur fonciere","Date mutation","Type de voie","Voie","Commune","Type local","Code voie", "Code commune","Code departement","id_vente", "No voie"])
    y = df_clean["Valeur fonciere"]
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
    xgb = XGBRegressor()
    model = xgb.fit(X_train, y_train)
    return model

# Fonction pour l'image

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path):
    img_html = f"<img src='data:image/png;base64,{img_to_bytes(img_path)}' class='img-fluid'>"
    return img_html

def load_css(file_name=".streamlit/color.css"):
    with open(file_name) as f:
        css = f"<style>{f.read()}</style>"
    return css
